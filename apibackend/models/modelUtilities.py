from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify
from auth.authUtilities import getPermissionFlags 
# from models.models import PeakHour

def getJSCompatibleTimeStamp(dt):
    if(dt is None): return None
    return int(dt.timestamp() * 1000)

def fetchPageMetaData(current_user, targetTableClass):
    try:
        if(targetTableClass is None):
            raise Exception("Insufficient Data Sent from Client!!")

        readPermission = False
        writePermission = False

        from .models import PeakHour # Lazy Import.
        allowedWriteRoles = eval(targetTableClass).get_write_permissions()
        allowedReadRoles = eval(targetTableClass).get_read_permissions()
        # print(allowedWriteRoles)

        user_info = {}
        if current_user:
            # Get additional claims
            claims = get_jwt()
            user_info = claims.get("user_info", {})

        readPermission, writePermission = getPermissionFlags(allowedReadRoles, allowedWriteRoles, user_info)


        data = {
            "readPermission": readPermission,
            "writePermission": writePermission,            
        }

        jsonData = {
            "success": True,
            "summary":"Meta Data Fetched",
            "message": "Meta Data Fetched successfully.",
            "data": data,
            "type": "success"
        }

        # print("Works here")
        return jsonify(jsonData), 200

    except Exception as e:
        print(e)

        jsonData = {
            "success": False,
            "type": "error",
            "summary":"Something went wrong",
            "message": "An error occurred while fetching data.",
            "error": str(e)
        }

        return jsonify(jsonData), 500