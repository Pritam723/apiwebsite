
from flask import jsonify, send_file, current_app as app

# from datetime import datetime
from models.models import db, Tenders
from auth.authUtilities import getPermissionFlags 
from flask_jwt_extended import get_jwt
from .tenderUtilities import ResponseException
import time
from permissions.pagePermissions import PAGE_PERMISSIONS
from permissions.roles import Roles
from .tenderUtilities import saveWithUniqueName
from datetime import  datetime, timedelta
# from enum import Enum
import pytz
import os
import shutil


def fetchTender(targetTableClass, tenderId):
    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass) or (not tenderId)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = Tenders

        #########################   No need to Check Read-Write Permissions here ###################################################
       
        #############################################################################################################


        product = TableClass.query.filter(TableClass.id == tenderId).first()

        if not product:
            raise ResponseException({"message" : "Entry not found!!", "summary" : "Something went wrong", "status" : 500})

        uploadPath = app.config['UPLOAD_FOLDER'] + TableClass.get_upload_path()
        print(uploadPath)

        os.makedirs(uploadPath + "\TenderFiles", exist_ok=True)


        TenderFilesPath = uploadPath + "\TenderFiles"

        for filePath in product.tenderFilesStored:
            fullFilePath = uploadPath + "\\" + filePath
            # print(fullFilePath)
            shutil.copy(fullFilePath, TenderFilesPath)


        shutil.make_archive(TenderFilesPath, 'zip', TenderFilesPath)

        # return None
        # Validate file existence
        shutil.rmtree(TenderFilesPath)

        product.downloadedTimes += 1  # Increment the attribute (replace 'count' with your actual column name)
        db.session.commit()


        return send_file(uploadPath + "\TenderFiles.zip", as_attachment=True)

    
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

def fetchAllTenders(targetTableClass):

    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = Tenders
        # yearObj = datetime(int(year), 1, 1)

        #########################   No need to Check Read-Write Permissions here ###################################################
       
        #############################################################################################################


        # tenders = TableClass.query.all()
        tenders = TableClass.query.order_by(TableClass.bidStartDate).all()

        data = {
            "data": [ row.serialize for row in tenders ],
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


def deleteOneTender(current_user, tenderId, targetTableClass):
    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass) or (not tenderId)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = Tenders
 
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


        product = TableClass.query.filter_by(id=tenderId).first()
        if product:
            db.session.delete(product)
            db.session.commit()
      

        data = {
            "info": f"Item {tenderId} deleted from {targetTableClass}"
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



def addFilesToNewTender(product, files, TableClass, userId):

    # time.sleep(5)

    # print(product)
    # We still need to add the user (uploadedBy), fileName, filePath,
    # fileSize, isMigrated, isDeleted etc.

    timeNow = datetime.today()
    timeNow = timeNow.replace(microsecond=0)

    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timeNow = IST.localize(timeNow)


    files_to_add_actual = []
    files_to_add_stored = []

    uploadPath = TableClass.get_upload_path()
    uploadFolder = app.config['UPLOAD_FOLDER'] + uploadPath


    if(not files):
        raise ResponseException({"message" : "Must upload at least one file!!", "summary" : "Something went wrong", "status" : 500})

    
    for file in files:
        # print(file)
        # {'fileName': 'download (2).csv',
        # 'lastModified': 1738572257266,
        # 'size': 252,
        # 'filetype': 'text/csv',
        # 'extension': 'csv',
        # 'base64Data': 'data:text/csv;base64,77u/IkNvZG...9yaWVzIiwiNzMi'}

        newFileName = saveWithUniqueName(uploadFolder, file)
        # files_to_add.append(f"{uploadPath}\{newFileName}")
        files_to_add_actual.append(file["fileName"])
        files_to_add_stored.append(f"{newFileName}")
        
        # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
        # id will be auto generated uuid

    product["uploadedBy"] = userId
    product["uploadedOn"] = timeNow
    product["tenderFilesActual"] = files_to_add_actual
    product["tenderFilesStored"] = files_to_add_stored
    product["downloadedTimes"] = 0

    # description
    # nitRef
    # bidStartDate 
    # bidEndDate 
    # bidOpeningDate 
    # tenderFilesActual 
    # tenderFilesStored
    # downloadedTimes

    # print(product)
    product_to_add = TableClass(**product)
    

    # Add all products to the session
    # print(products_to_add)
    db.session.add(product_to_add)
    db.session.commit()
    # Print inserted IDs
    productIDs = [product_to_add.id] # Dot Notation works because it is an Object not Dictionary.
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

    

def addFilesToExistingTender(product, files, TableClass, userId):
    # print(product)
    
    # time.sleep(5)

    # print(product)
    # We still need to add the user (uploadedBy), fileName, filePath,
    # fileSize, isMigrated, isDeleted etc.

    timeNow = datetime.today()
    timeNow = timeNow.replace(microsecond=0)

    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timeNow = IST.localize(timeNow)
    
    files_to_add_actual = []
    files_to_add_stored = []

    uploadPath = TableClass.get_upload_path()
    uploadFolder = app.config['UPLOAD_FOLDER'] + uploadPath


    # if(not files):
    #     raise ResponseException({"message" : "Must upload at least one file!!", "summary" : "Something went wrong", "status" : 500})


    for file in files:
        # print(file)
        # {'fileName': 'download (2).csv',
        # 'lastModified': 1738572257266,
        # 'size': 252,
        # 'filetype': 'text/csv',
        # 'extension': 'csv',
        # 'base64Data': 'data:text/csv;base64,77u/IkNvZG...9yaWVzIiwiNzMi'}

        newFileName = saveWithUniqueName(uploadFolder, file)
        # files_to_add.append(f"{uploadPath}\{newFileName}")
        files_to_add_actual.append(file["fileName"])
        files_to_add_stored.append(f"{newFileName}")
        
        # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
        # id will be auto generated uuid

    tender = TableClass.query.get(product["id"])  # Fetch the row by ID
    if tender:
        tender.tenderFilesActual = list(tender.tenderFilesActual + files_to_add_actual)  # Merge and remove duplicates
        tender.tenderFilesStored = list(tender.tenderFilesStored + files_to_add_stored)  # Merge and remove duplicates

        tender.uploadedBy = userId

        # description
        # nitRef
        # bidStartDate 
        # bidEndDate 
        # bidOpeningDate 
        # tenderFilesActual 
        # tenderFilesStored
        # downloadedTimes

        tender.description = product["description"]
        tender.nitRef = product["nitRef"]
        tender.bidStartDate = product["bidStartDate"]
        tender.bidEndDate = product["bidEndDate"]
        tender.bidOpeningDate = product["bidOpeningDate"]

        db.session.commit()  # Save changes

    productIDs = [product["id"]] # Dot Notation works because it is an Object not Dictionary.
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


def addNewTender(current_user, product, files, targetTableClass):
    print(current_user, product, len(files), targetTableClass)
    # return None
    # Database Logic to add data in Database.
    try:

        if(not (product and targetTableClass)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})


        TableClass = Tenders

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
        if(product.get("id") is None):
            print("Adding Tender")
            return addFilesToNewTender(product, files, TableClass, userId)
        else:
            print("Updating Tender")
            return addFilesToExistingTender(product, files, TableClass, userId)
    
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