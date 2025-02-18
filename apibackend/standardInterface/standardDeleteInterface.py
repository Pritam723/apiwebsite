from flask import jsonify, current_app as app
from models.models import db, getModelClass
from auth.authUtilities import getPermissionFlags 
from flask_jwt_extended import get_jwt

from .standardInterfaceUtilities import ResponseException

def deleteFromStandardTable(current_user, productIdToDelete, targetTableClass):
    try:
        # m = 0/0 # Generating Error
        if((not targetTableClass) or (not productIdToDelete)):
            raise ResponseException({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        TableClass = getModelClass(targetTableClass)

        #########################   Check Read-Write Permissions ###################################################
        readPermission = False
        writePermission = False


        allowedWriteRoles = TableClass.get_write_permissions()
        allowedReadRoles = TableClass.get_read_permissions()
        # print(allowedWriteRoles)

        user_info = {}
        if current_user:
            # Get additional claims
            claims = get_jwt()
            user_info = claims.get("user_info", {})

        readPermission, writePermission = getPermissionFlags(allowedReadRoles, allowedWriteRoles, user_info)

        if(writePermission == False):
            raise ResponseException({"message" : "You do not have permission to perform the action!!", "summary" : "Something went wrong", "status" : 403})
        #############################################################################################################
        
        product = TableClass.query.filter_by(id=productIdToDelete).first()
        if product:
            db.session.delete(product)
            db.session.commit()
      

        data = {
            "info": f"Item {productIdToDelete} deleted from {targetTableClass}"
        }

        jsonData = {
            "success": True,
            "summary":"Deletion Successful",
            "message": "File deleted.",
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