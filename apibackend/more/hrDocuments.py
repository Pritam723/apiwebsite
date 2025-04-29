from flask import jsonify, current_app as app

# from datetime import datetime
from models.models import db, HRDocuments
from auth.authUtilities import getPermissionFlags 
from flask_jwt_extended import get_jwt
import time
from permissions.pagePermissions import PAGE_PERMISSIONS
from permissions.roles import Roles
from datetime import  datetime, timedelta
# from enum import Enum
import pytz
import os

import base64
from codecs import encode
import uuid

def jsDateStrToTimeZoneAwareDate(fileDate):
    
    # 'fileDate': '2025-02-04T18:30:00.000Z'
    # Example: A naive datetime object (without timezone)
    # naive_dt = datetime(2025, 2, 5, 12, 30, 0)  # 12:30 PM without timezone

    naive_dt = datetime.strptime(fileDate, "%Y-%m-%dT%H:%M:%S.%fZ")
    naive_dt = naive_dt + timedelta(hours = 5, minutes = 30)
    # Define the correct timezone (e.g., Asia/Kolkata)
    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timezone_aware_dt = IST.localize(naive_dt)
    return timezone_aware_dt

class ResponseException(Exception):
    pass



# Useful while Saving data to FileSystem.
def saveWithUniqueName(uploadFolder, file, typeOfDocument):
    print(uploadFolder)
    os.makedirs(uploadFolder, exist_ok=True)
    fileName = file["fileName"]
    base, ext = os.path.splitext(fileName)  # Split filename and extension

    fileName = typeOfDocument + ext

    filepath = os.path.join(uploadFolder, fileName)
    # counter = 1
    print(filepath)

    # Check if file exists and generate a unique name
    # while os.path.exists(filepath):
    #     filepath = os.path.join(uploadFolder, f"{base} ({counter}){ext}")
    #     counter += 1

    base64_str = file["base64Data"].split(';base64')[1] # No need to worry ';' is not a valid base64 Character.
    bytes_obj = encode(base64_str, 'utf-8')
    binary_obj = base64.decodebytes(bytes_obj)

    with open(filepath, "wb") as fh:
        fh.write(binary_obj)

    return os.path.basename(filepath)  # Return saved file name



######################################################## Change Logic for HR Documents #############################################################

def fetchAllHRDocuments(targetTableClass):

    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = HRDocuments
        # yearObj = datetime(int(year), 1, 1)

        #########################   No need to Check Read-Write Permissions here ###################################################
       
        #############################################################################################################


        hrDocuments = TableClass.query.all()

        data = {
            "data": [ row.serialize for row in hrDocuments ],
            # "dataInfo": dataInfo
        }

        jsonData = {
            "success": True,
            "summary":"Fetch Successful",
            "message": "Data Fetched successfully.",
            "data": data,
            "type": "success"
        }

        # print("Works here")

        return jsonify(jsonData), 200

    
    except ResponseException as e:
  
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]
    
    except Exception as e:

        print(e)
        print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500


def addNewHRDocument(current_user, product, files, targetTableClass):
    print(current_user, product, len(files), targetTableClass)
    # return None
    # Database Logic to add data in Database.

    checkExtension = {
        "OgranizationalChart" : ".pdf",
        "ISO_27001": ".pdf",
        "ISO_45001": ".pdf",
        "ISO_14001": ".pdf",
        "ISO_9001": ".pdf",
        "IMS_Policy": ".pdf",
        "EmpList": ".pdf",
        "EmployeeDirectory": ".pdf",
        "ERLDC_Empanelled_Hospitals": ".pdf",
        "WB_Power_Map": ".pdf",
        "Sikkim_Power_Map": ".pdf",
        "Jharkhand_Power_Map": ".pdf",
        "Odisha_Power_Map": ".pdf",
        "Bihar_Power_Map": ".pdf",
        "DVC_Power_Map": ".pdf",
        "ER_Power_Map": ".pdf",
        "ERLDC_Outage_Procedure": ".pdf",
        "PublicInformationOfficers": ".pdf",
        "InformationAvailableInElectronicForm": ".pdf",
    }












    try:

        if(not (product and targetTableClass)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})


        TableClass = HRDocuments

        # write_premissions = eval(targetTableClass).get_write_permissions()
        # print(write_premissions)
        # Check this with the current user
        # If all checks are passed, then only go ahead with the update/insert query.

        # print(product.get("id"))

        #########################   Check Read-Write Permissions ###################################################
        readPermission = False
        writePermission = False


        # allowedWriteRoles = TableClass.get_write_permissions()
        # allowedReadRoles = TableClass.get_read_permissions()
        # print(allowedWriteRoles)
        permissions = PAGE_PERMISSIONS.get(targetTableClass, {'READ_PERMISSION': [Roles.SUPER_ADMIN],'WRITE_PERMISSION': [Roles.SUPER_ADMIN]})
        allowedReadRoles = permissions['READ_PERMISSION']
        allowedWriteRoles = permissions['WRITE_PERMISSION']
        # {'READ_PERMISSION': [],'WRITE_PERMISSION': []}

        user_info = None
        if current_user:
            # Get additional claims
            claims = get_jwt()
            user_info = claims.get("user_info", None)

        readPermission, writePermission = getPermissionFlags(allowedReadRoles, allowedWriteRoles, user_info)

        if(writePermission == False):
            raise ResponseException({"message" : "You do not have permission to perform the action!!", "summary" : "Something went wrong", "status" :403})

        #############################################################################################################

        userId = user_info.get("user_id", None)

        typeOfDocument = product['typeOfDocument']

        # First check if there is any entry with this typeOfDocument.
    

        # Example values
        
        # timeNow = datetime.today()
        # timeNow = timeNow.replace(microsecond=0)

        # IST = pytz.timezone("Asia/Kolkata")
        # # Localize the naive datetime to IST
        # timeNow = IST.localize(timeNow)


        uploadPath = "/files"

        print(app.static_folder)

        # print("Logging here...")
        
        # uploadFolder = app.config['UPLOAD_FOLDER']
        uploadFolder = app.static_folder + uploadPath

        file = files[0]

        fileName = file["fileName"]
        base, ext = os.path.splitext(fileName)  # Split filename and extension
        
        expectedExtension = checkExtension.get(typeOfDocument, None)

        if(expectedExtension is None):
            raise ResponseException({"message" : f"No matching extension found!!", "summary" :  f"FNo matching extension found!!", "status" :500})


        if(ext != expectedExtension):
            raise ResponseException({"message" : f"File Extension must be {expectedExtension}!!", "summary" :  f"File Extension must be {expectedExtension}!!", "status" :500})

        
        newFileName = saveWithUniqueName(uploadFolder, file, typeOfDocument)

    
        # Step 1: Delete existing document with same typeOfDocument
        existing_doc = HRDocuments.query.filter_by(typeOfDocument=typeOfDocument).first()
        if existing_doc:
            db.session.delete(existing_doc)
            db.session.commit()

        # Step 2: Insert new document
        new_doc = HRDocuments(
            id=str(uuid.uuid4()),
            typeOfDocument=typeOfDocument,
            uploadedOn=jsDateStrToTimeZoneAwareDate(product['uploadedOn']),
            uploadedBy=userId
        )
        db.session.add(new_doc)
        db.session.commit()


        productIDs = [new_doc.id] # Dot Notation works because it is an Object not Dictionary.
        # print(productIDs)

        data = {
            "productIDs": productIDs,
        }

        jsonData = {
            "success": True,
            "summary":"Upload Successful",
            "message": "File saved successfully.",
            "data": data,
            "type": "success"
        }

        return jsonify(jsonData), 200




    except ResponseException as e:
  
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]

    except Exception as e:
        # print(e)
        # print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500