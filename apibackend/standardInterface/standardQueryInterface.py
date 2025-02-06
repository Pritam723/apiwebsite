from flask import jsonify, current_app as app
from datetime import datetime
from models.models import db,Task, PeakHour
import os

def fetchDataFromStandardTable(filterBy, filterRange,targetTableClass):
    
    try:
        # m = 0/0 # Generating Error
        if(not (targetTableClass)):
            raise Exception("Insufficient Data Sent from Client!!")

        products = eval(targetTableClass).query.all()
            

        print(products)
        data = {
            "products": [ row.serialize for row in products ],
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
            "message": "An error occurred while fetching data.",
            "error": str(e)
        }

        return jsonify(jsonData), 500