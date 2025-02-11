from flask import jsonify, current_app as app
from .standardInterfaceUtilities import preprocessDataBeforeAddition,preprocessDataBeforeUpdate, saveWithUniqueName
from datetime import datetime
from models.models import db,Task, PeakHour

def addDataToStandardTable(product, uploadPoints, files, targetTableClass):
    preprocessDataBeforeAddition(product, uploadPoints)
    print("Data Preprocessed before addition")
    # print(product)
    # We still need to add the user (uploadedBy), fileName, filePath,
    # fileSize, isMigrated, isDeleted etc.




    products_to_add = []

    # print("Path to upload: ")
    # print(os.getcwd())
    uploadPath = eval(targetTableClass).get_upload_path()
    uploadFolder = app.config['UPLOAD_FOLDER'] + uploadPath
    for file in files:
        # print(file)
        # {'fileName': 'download (2).csv',
        # 'lastModified': 1738572257266,
        # 'size': 252,
        # 'filetype': 'text/csv',
        # 'extension': 'csv',
        # 'base64Data': 'data:text/csv;base64,77u/IkNvZG...9yaWVzIiwiNzMi'}

        newFileName = saveWithUniqueName(uploadFolder, file)

        # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
        # id will be auto generated uuid

        product["fileName"] = file["fileName"]
        product["size"] = str(file["size"]) # In Bytes
        product["uploadedBy"] = "Current User"
        product["isMigrated"] = False
        product["isDeleted"] = False
        product["filePath"] = f"{uploadPath}\{newFileName}"

        # print(product)
        product_to_add = eval(targetTableClass)(**product)
        products_to_add.append(product_to_add)

    # Add all products to the session
    # print(products_to_add)
    db.session.add_all(products_to_add)
    db.session.commit()
    # Print inserted IDs
    productIDs = [product.id for product in products_to_add] # Dot Notation works because it is an Object not Dictionary.
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

def updateDataToStandardTable(product, uploadPoints, files, targetTableClass):
    
    preprocessDataBeforeUpdate(product, uploadPoints)
    print("Data Preprocessed before updation")
    # print(product)
    # We still need to add the user (uploadedBy), fileName, filePath,
    # fileSize, isMigrated, isDeleted etc.

    # write_premissions = eval(targetTableClass).get_write_permissions()
    # print(write_premissions)
    # Check this with the current user
    # If all checks are passed, then only go ahead with the update/insert query.

    # print(product.get("id"))
    
    
    uploadPath = eval(targetTableClass).get_upload_path()
    uploadFolder = app.config['UPLOAD_FOLDER'] + uploadPath


    old_product = eval(targetTableClass).query.get(product["id"])  # Fetch entry by ID
    if old_product is None:
        raise Exception("Could not able to find the Item!!")

    # First change the parameters of old_product with the new_product. Do not
    # Change the ID obviously. Also after this do not forget to add the file
    # Details.

    # Do not worry, all the datas of new_product are already preprocessed. Ex. lastUpdatedOn
    # Will be added there.
    for key in product:
        # Do not take ID of new_product. Because it is same anyway.
        # print(key)
        if(key == "id"):
            continue
        # print("Changing value to ")
        # print(product[key])
        # old_product.key = product[key] # Dot notation for Object. Subscript for Dictionary.
        # print("Is it done?")
        # print(old_product.key)

        setattr(old_product, key, product[key]) 

    file = files[0]
    # print(file)
    # {'fileName': 'download (2).csv',
    # 'lastModified': 1738572257266,
    # 'size': 252,
    # 'filetype': 'text/csv',
    # 'extension': 'csv',
    # 'base64Data': 'data:text/csv;base64,77u/IkNvZG...9yaWVzIiwiNzMi'}
    newFileName = saveWithUniqueName(uploadFolder, file)

    setattr(old_product, "fileName", file["fileName"])
    setattr(old_product, "size", str(file["size"])) # In Bytes
    setattr(old_product, "uploadedBy", "Current User")
    setattr(old_product, "isMigrated", False)
    setattr(old_product, "isDeleted", False)
    setattr(old_product, "filePath", f"{uploadPath}\{newFileName}")

    
    # Now we can commit.
    db.session.commit()  # Save changes
    
    data = {
        "productIDs": [old_product.id],
    }

    jsonData = {
        "success": True,
        "summary":"Update Successful",
        "message": "File updated successfully.",
        "data": data,
        "type": "success"
    }

    return jsonify(jsonData), 200


def dataToStandardTable(product, uploadPoints, files, targetTableClass):
    # Database Logic to add data in Database.
    try:

        if(not (product and files and targetTableClass)):
            raise Exception("Insufficient Data Sent from Client!!")


        # write_premissions = eval(targetTableClass).get_write_permissions()
        # print(write_premissions)
        # Check this with the current user
        # If all checks are passed, then only go ahead with the update/insert query.

        # print(product.get("id"))

        if(product.get("id") is None):
            print("Adding Data")
            return addDataToStandardTable(product, uploadPoints, files, targetTableClass)
        else:
            print("Updating Data")
            return updateDataToStandardTable(product, uploadPoints, files, targetTableClass)
    
    except Exception as e:
        # print(e)

        jsonData = {
            "success": False,
            "type": "error",
            "summary":"Something went wrong",
            "message": "An error occurred while uploading.",
            "error": str(e)
        }

        return jsonify(jsonData), 500
