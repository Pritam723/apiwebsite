from flask import jsonify, send_file, current_app as app
from datetime import datetime
from models.models import getModelClass
import os
from .standardInterfaceUtilities import getQueryRange, formatDateWithSuffix
from auth.authUtilities import getPermissionFlags 
from flask_jwt_extended import get_jwt
import time
from .standardInterfaceUtilities import ResponseException
from permissions.pagePermissions import PAGE_PERMISSIONS
from permissions.roles import Roles

def downloadFromStandardTable(current_user, productIdToDownload, targetTableClass):
    # print(productIdToDownload, targetTableClass)
    try:
        # m = 0/0 # Generating Error
        if((not targetTableClass) or (not productIdToDownload)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})
        

        TableClass = getModelClass(targetTableClass)



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

        # print(allowedReadRoles)
        # print(user_info)


        if(readPermission == False):
            raise ResponseException({"message" : "You do not have permission to fetch the Data!!", "summary" : "Something went wrong", "status" : 403})

        #############################################################################################################

        product = TableClass.query.filter_by(id=productIdToDownload).first()
        
        if not product:
            raise ResponseException({"message" : "Entry not found!!", "summary" : "Something went wrong", "status" : 500})

        uploadPath = app.config['UPLOAD_FOLDER'] + product.filePath
        # print(uploadPath)
        # Validate file existence
        return send_file(uploadPath, as_attachment=True)

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



def fetchDataFromStandardTable(current_user, filterOptions, targetTableClass):
    # time.sleep(2) # Introducing delay.
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
    print(current_user, filterOptions, targetTableClass)
   
    try:
        # m = 0/0 # Generating Error
        if(not targetTableClass):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = getModelClass(targetTableClass)

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

        if(readPermission == False):
            raise ResponseException({"message" : "You do not have permission to fetch the Data!!", "summary" : "Something went wrong", "status" : 500})
        #############################################################################################################

        queryStartDateObj, queryEndDateObj = getQueryRange(filterOptions)
        # print(queryStartDateObj, queryEndDateObj)
        dataInfo = ""
        if((queryStartDateObj is None) or (queryEndDateObj is None)):
            # Fetch all data. No filtering.
            products = TableClass.query\
                .order_by(TableClass.fileDate.desc())\
                    .all()
            # print("hi")
            # print(products)
        else:
            # Apply Filters here based on queryStartDateObj, queryEndDateObj.
            # Actually the way we have stored the data, we can simply compare with TableName.startDateToFilter
            products = TableClass.query.filter(TableClass\
                                .startDateToFilter.between(queryStartDateObj, queryEndDateObj))\
                                        .order_by(TableClass.fileDate.desc())\
                                            .all()
            # dataInfo = f"Showing Data From {queryStartDateObj.strftime('%d-%m-%Y')} to {queryEndDateObj.strftime('%d-%m-%Y')}."
            
            # print("hello")
            # print(products)
            dataInfo = f"Showing Data From {formatDateWithSuffix(queryStartDateObj)} to {formatDateWithSuffix(queryEndDateObj)}."

        # print(products)

        data = {
            "products": [ row.serialize for row in products ],
            "dataInfo": dataInfo
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