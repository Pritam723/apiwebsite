from flask import jsonify, current_app as app
from .standardInterfaceUtilities import preprocessData
from datetime import datetime
from models.models import db,Task, PeakHour
import base64
from codecs import encode
import os

def save_with_unique_name(uploadFolder, file):
    os.makedirs(uploadFolder, exist_ok=True)
    fileName = file["fileName"]
    base, ext = os.path.splitext(fileName)  # Split filename and extension
    filepath = os.path.join(uploadFolder, fileName)
    counter = 1
    print(filepath)

    # Check if file exists and generate a unique name
    while os.path.exists(filepath):
        filepath = os.path.join(uploadFolder, f"{base} ({counter}){ext}")
        counter += 1

    base64_str = file["base64Data"].split(';base64')[1] # No need to worry ';' is not a valid base64 Character.
    bytes_obj = encode(base64_str, 'utf-8')
    binary_obj = base64.decodebytes(bytes_obj)

    with open(filepath, "wb") as fh:
        fh.write(binary_obj)

    return os.path.basename(filepath)  # Return saved file name


def addDataToStandardTable(product, files, targetTableClass):
    # Database Logic to add data in Database.
    try:

        if(not (product and files and targetTableClass)):
            raise Exception("Insufficient Data Sent from Client!!")

        preprocessData(product)
        # print(product)
        # We still need to add the user (uploadedBy), fileName, filePath,
        # fileSize, isMigrated, isDeleted etc.

        # write_premissions = eval(targetTableClass).get_write_permissions()
        # print(write_premissions)
        # Check this with the current user

        products_to_add = []

        # print("Path to upload: ")
        # print(os.getcwd())
        uploadFolder = app.config['UPLOAD_FOLDER'] + eval(targetTableClass).get_upload_path()

        for file in files:
            # print(file)
            # {'fileName': 'download (2).csv',
            # 'lastModified': 1738572257266,
            # 'size': 252,
            # 'filetype': 'text/csv',
            # 'extension': 'csv',
            # 'base64Data': 'data:text/csv;base64,77u/IkNvZG...9yaWVzIiwiNzMi'}

            newFileName = save_with_unique_name(uploadFolder, file)

            # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
            # id will be auto generated uuid

            product["fileName"] = file["fileName"]
            product["size"] = str(file["size"]) # In Bytes
            product["uploadedBy"] = "Current User"
            product["isMigrated"] = False
            product["isDeleted"] = False
            product["filePath"] = f"{uploadFolder}\{newFileName}"

            product_to_add = eval(targetTableClass)(**product)
            products_to_add.append(product_to_add)

        # Add all products to the session
        db.session.add_all(products_to_add)
        db.session.commit()
        # Print inserted IDs
        productIDs = [product.id for product in products_to_add]
        print(productIDs)

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
    
    except Exception as e:
        print(e)

        jsonData = {
            "success": False,
            "type": "error",
            "summary":"Something went wrong",
            "message": "An error occurred while uploading.",
            "error": str(e)
        }

        return jsonify(jsonData), 500
