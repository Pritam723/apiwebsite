from flask import jsonify, send_file, current_app as app
from datetime import datetime
from models.models import db,Task, PeakHour
import os
from .standardInterfaceUtilities import getQueryRange, formatDateWithSuffix

def downloadFromStandardTable(productIdToDownload, targetTableClass):
    print(productIdToDownload, targetTableClass)
    try:
        # m = 0/0 # Generating Error
        if((not targetTableClass) or (not productIdToDownload)):
            raise Exception("Insufficient Data Sent from Client!!")
        
        product = eval(targetTableClass).query.filter_by(id=productIdToDownload).first()
        
        if not product:
            raise Exception("Entry not found!!")
      

        uploadPath = app.config['UPLOAD_FOLDER'] + product.filePath
        print(uploadPath)
        # Validate file existence
        return send_file(uploadPath, as_attachment=True)

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

def fetchDataFromStandardTable(filterOptions, targetTableClass):
    
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}

    try:
        # m = 0/0 # Generating Error
        if(not targetTableClass):
            raise Exception("Insufficient Data Sent from Client!!")

        queryStartDateObj, queryEndDateObj = getQueryRange(filterOptions)

        # print(queryStartDateObj, queryEndDateObj)
        dataInfo = ""
        if((queryStartDateObj is None) or (queryEndDateObj is None)):
            # Fetch all data. No filtering.
            products = eval(targetTableClass).query\
                .order_by(eval(targetTableClass).fileDate.desc())\
                    .all()
        else:
            # Apply Filters here based on queryStartDateObj, queryEndDateObj.
            # Actually the way we have stored the data, we can simply compare with TableName.startDateToFilter
            products = eval(targetTableClass).query.filter(eval(targetTableClass)\
                                .startDateToFilter.between(queryStartDateObj, queryEndDateObj))\
                                        .order_by(eval(targetTableClass).fileDate.desc())\
                                            .all()
            # dataInfo = f"Showing Data From {queryStartDateObj.strftime('%d-%m-%Y')} to {queryEndDateObj.strftime('%d-%m-%Y')}."
            

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