from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity



from flask_cors import CORS
from datetime import timedelta

# For .env file reference.
import os
from dotenv import load_dotenv

# Imports from other modules.
from auth import authentication
from standardInterface.standardUploadInterface import dataToStandardTable
from standardInterface.standardDeleteInterface import deleteFromStandardTable
from standardInterface.standardQueryInterface import fetchDataFromStandardTable, downloadFromStandardTable
from standardInterface.standardInterfaceUtilities import getFinancialYearList

from models.models import db, Task
from models.modelUtilities import fetchPageMetaData


# For DB Connection.
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Reading the .env file.
load_dotenv(dotenv_path=".env")

# Setting Up DB
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
encoded_db_password = db_password.replace("@", "%40")
db_location = os.getenv('DB_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{encoded_db_password}@{db_location}"
db.init_app(app)


# Setting up File Upload Settings
UPLOAD_FOLDER = 'uploads'  # Directory to store files
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # Limit file size to 25MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)



@app.route('/')
def hello():
    # print(os.getenv('JWT_KEY'))
    # print(len(os.getenv('JWT_KEY')))
    return 'Hello, World!'


############################# Utility Functions #####################################

@app.route("/getFYList", methods=["GET"])
def getFYList():
    return getFinancialYearList(), 200

#######################################################################################


@app.route("/login", methods=["POST"])
def login():
    # print("here I am")
    user_id = request.json.get("email", None)
    password = request.json.get("password", None)
    print(user_id, password)
    token = authentication.create_token(user_id, password)
    # print(token)
    return token

# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@app.route("/refresh_token", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    token = authentication.refresh_token(identity)
    return token

################################## Operations on Standard Table ########################

@app.route("/addStandardData", methods = ["GET","POST"])
def addStandardData():
    print("Adding/Updating Data")

    product = request.json.get("product", None)
    uploadPoints = request.json.get("uploadPoints", {})
    files = request.json.get("files", None)
    targetTableClass = request.json.get("targetTableClass", None)
    # print(product)
    # print(uploadPoints)

    response = dataToStandardTable(product, uploadPoints, files, targetTableClass)
    
    return(response)

@app.route("/deleteStandardData", methods = ["GET","POST"])
def deleteStandardData():
    print("Deleting Data")

    productIdToDelete = request.json.get("productIdToDelete", None)
    targetTableClass = request.json.get("targetTableClass", None)

    response = deleteFromStandardTable(productIdToDelete, targetTableClass)
    
    return response

@app.route("/downloadStandardData", methods = ["GET", "POST"])
def downloadStandardData():
    print("Downloading Data")

    productIdToDownload = request.json.get("productIdToDownload", None)
    targetTableClass = request.json.get("targetTableClass", None)

    response = downloadFromStandardTable(productIdToDownload, targetTableClass)
    
    return response


@app.route("/fetchAllStandardData", methods = ["GET","POST"])
def fetchAllStandardData():
    # print("Fetching Data")

    filterOptions = request.json.get("filterOptions", {
        "filterBy": None,
        "filterRange": None,
        "filterFY": None,
        "filterQuarter": None,
        "defaultFiltering": None
    })

    # print(filterOptions)

    targetTableClass = request.json.get("targetTableClass", None)
    # print(product)

    response = fetchDataFromStandardTable(filterOptions, targetTableClass)
    
    return(response)


@app.route("/fetchStandardPageMetaData", methods = ["GET","POST"])
@jwt_required(optional=True)
def fetchStandardPageMetaData():
    current_user = get_jwt_identity()
    targetTableClass = request.json.get("targetTableClass", None)
   
    return fetchPageMetaData(current_user, targetTableClass)

    # if current_user:
    #     print(current_user)
    #     print("1 token")
    #     # Get additional claims
    #     claims = get_jwt()
    #     user_info = claims.get("user_info", {})

    #     print(user_info)
    # else:
    #     print("No token")

    # return "Hi"


########################################################################################

# main driver function
if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    print(db.Model)

    app.run(debug = True, port = 4001, host = "0.0.0.0")
