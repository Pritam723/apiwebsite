from flask import jsonify, current_app as app
from models.models import db, PeakHour


def deleteFromStandardTable(productIdToDelete, targetTableClass):
    try:
        # m = 0/0 # Generating Error
        if((not targetTableClass) or (not productIdToDelete)):
            raise Exception("Insufficient Data Sent from Client!!")
        
        product = eval(targetTableClass).query.filter_by(id=productIdToDelete).first()
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

    except Exception as e:
        print(e)

        jsonData = {
            "success": False,
            "type": "error",
            "summary":"Something went wrong",
            "message": "An error occurred while deleting data.",
            "error": str(e)
        }

        return jsonify(jsonData), 500