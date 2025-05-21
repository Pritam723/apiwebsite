
from flask import jsonify, current_app as app

# from datetime import datetime
from models.models import db, Albums
from auth.authUtilities import getPermissionFlags 
from flask_jwt_extended import get_jwt
from .albumUtilities import ResponseException
import time
from permissions.pagePermissions import PAGE_PERMISSIONS
from permissions.roles import Roles
from .albumUtilities import saveWithUniqueName
from datetime import  datetime, timedelta
# from enum import Enum
import pytz
from standardInterface.standardInterfaceUtilities import jsDateStrToTimeZoneAwareDate

def fetchAlbum(targetTableClass, albumId):
    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass) or (not albumId)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = Albums

        #########################   No need to Check Read-Write Permissions here ###################################################
       
        #############################################################################################################


        album = TableClass.query.filter(TableClass.id == albumId).first()



        data = {
            "data": {
                "title" : album.title,
                "images": album.images
            },
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

def fetchAllAlbums(targetTableClass, year):

    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass) or (not year)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = Albums
        yearObj = datetime(int(year), 1, 1)

        #########################   No need to Check Read-Write Permissions here ###################################################
       
        #############################################################################################################


        albums = TableClass.query.filter(TableClass.year == yearObj).all()

        print("Printing length of albums")
        print(len(albums))

        data = {
            "data": [ row.serialize for row in albums ],
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


def deleteAnAlbum(current_user, albumId, targetTableClass):
    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
   
    try:
        # m = 0/0 # Generating Error

        
        if((not targetTableClass) or (not albumId)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = Albums
 
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


        product = TableClass.query.filter_by(id=albumId).first()
        if product:
            db.session.delete(product)
            db.session.commit()
      

        data = {
            "info": f"Item {albumId} deleted from {targetTableClass}"
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


def addImagesToNewAlbum(product, files, TableClass, userId):

    # time.sleep(5)

    # print(product)
    # We still need to add the user (uploadedBy), fileName, filePath,
    # fileSize, isMigrated, isDeleted etc.

    timeNow = datetime.today()
    timeNow = timeNow.replace(microsecond=0)

    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timeNow = IST.localize(timeNow)

    files_to_add = []

    # print("Path to upload: ")
    # print(os.getcwd())
    uploadPath = "/images"

    print(app.static_folder)

    print("Logging here...")
    
    # uploadFolder = app.config['UPLOAD_FOLDER']
    uploadFolder = app.static_folder + uploadPath

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
        files_to_add.append(f"{newFileName}")
        
        # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
        # id will be auto generated uuid

    product["cover"] = files_to_add[0]
    product["uploadedBy"] = userId
    product["uploadedOn"] = timeNow

    product["images"] = files_to_add
    product["noImages"] = len(files_to_add)

    product["year"] = jsDateStrToTimeZoneAwareDate(product["year"])

    # year = str(product["year"])
    # product["year"] = datetime.strptime(year, "%Y")
    print(product["year"])

    print(type(product["year"]))

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

    

def addImagesToExistingAlbum(product, files, TableClass, userId):
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

    files_to_add = []

    # print("Path to upload: ")
    # print(os.getcwd())
    uploadPath = "/images"

    print(app.static_folder)

    print("Logging here...")
    
    # uploadFolder = app.config['UPLOAD_FOLDER']
    uploadFolder = app.static_folder + uploadPath
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
        files_to_add.append(f"{newFileName}")
        
        # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
        # id will be auto generated uuid


    album = TableClass.query.get(product["id"])  # Fetch the row by ID
    if album:
        album.noImages += len(files)  # Increment noImages
        album.images = list(set(album.images + files_to_add))  # Merge and remove duplicates
        album.title = product['title']
        album.year = product['year']
        album.uploadedBy = userId
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


def addNewAlbum(current_user, product, files, targetTableClass):
    print(current_user, product, len(files), targetTableClass)
    # return None
    # Database Logic to add data in Database.
    try:

        if(not (product and targetTableClass)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})


        TableClass = Albums

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
            print("Adding Album")
            return addImagesToNewAlbum(product, files, TableClass, userId)
        else:
            print("Updating Album")
            return addImagesToExistingAlbum(product, files, TableClass, userId)
    
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