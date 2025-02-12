from flask_jwt_extended import get_jwt
from flask import jsonify
from auth.authUtilities import getPermissionFlags 
# from models.models import PeakHour

def getJSCompatibleTimeStamp(dt):
    if(dt is None): return None
    return int(dt.timestamp() * 1000)

def fetchPageMetaData(current_user, targetTableClass):
    try:
        # m = 0/0 # Generating Exception.
        if(targetTableClass is None):
            raise Exception({"message" : "Insufficient Data Sent from Client!!", "summary" : "Something went wrong", "status" : 500})

        readPermission = False
        writePermission = False

        from .models import getModelClass # Lazy Import.
        TableClass = getModelClass(targetTableClass)

        allowedWriteRoles = TableClass.get_write_permissions()
        allowedReadRoles = TableClass.get_read_permissions()

        multipleUploads = TableClass.get_multiple_upload_flag()

        uploadPoints = TableClass.get_upload_points()
        custom_uploaded_on_flag = TableClass.get_custom_uploaded_on_flag()
        uploadPoints["uploadedOn"] = custom_uploaded_on_flag

        dataToDisplay = TableClass.get_data_to_display()
        sortInUse = TableClass.get_sort_in_use()
        filtersInUse = TableClass.get_filters_in_use()
        defaultFilterning = TableClass.get_default_filter()

        # print(allowedWriteRoles)

        user_info = {}
        if current_user:
            # Get additional claims
            claims = get_jwt()
            user_info = claims.get("user_info", {})

        readPermission, writePermission = getPermissionFlags(allowedReadRoles, allowedWriteRoles, user_info)


        dynamicMetaData = {
            "readPermission": readPermission,
            "writePermission": writePermission,
            "multipleUploads": multipleUploads,
            "uploadPoints": uploadPoints,
            "dataToDisplay": dataToDisplay,
            "sortInUse": sortInUse,
            "filtersInUse": filtersInUse,
            "defaultFiltering": defaultFilterning,
        }



        data = {
            "dynamicMetaData" : dynamicMetaData          
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
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]