from flask import Flask, request, send_from_directory, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import get_jwt_identity

# For websocket connection.
from flask_socketio import SocketIO, send
import time
from scheduledTasks.realTimeSCADA import getSCADADATA

from flask_cors import CORS
from datetime import timedelta

# For .env file reference.
import os
from dotenv import load_dotenv

# Imports from other modules.
from auth.authentication import create_token, register_user, register_user_verify, forgot_password, forgot_password_verify
from standardInterface.standardUploadInterface import dataToStandardTable
from standardInterface.standardDeleteInterface import deleteFromStandardTable
from standardInterface.standardQueryInterface import fetchDataFromStandardTable, downloadFromStandardTable
from standardInterface.standardInterfaceUtilities import getFinancialYearList

from models.models import db
from models.modelUtilities import fetchPageMetaData
from RUN_DB_MIGRATION import runMigration





# For DB Connection.
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Uses the default "static/" folder

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
# CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})

CORS(app, resources={r"/*": {"origins": ["http://localhost:3001", "http://10.3.101.179:3001"]}})


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)


###################################### Setting up the websocket. ##################################
# socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3001", "http://10.3.101.179:3001"])
# @socketio.on("connect")
# def handle_connect():
#     data = getSCADADATA()
#     print(data)
#     time.sleep(2)
#     socketio.emit("message", {"data": data})

# @app.route('/testSocket', methods=["POST"])
# def send_updates():
#     print("Here")
    
#     # Get JSON data from request
#     data = request.get_json()
#     print("Received Data:", data)  # Debugging
    
#     # Emit WebSocket message
#     socketio.emit("message", {"data": data})
#     return jsonify({"message": "Data sent successfully"}), 200

# @socketio.on("disconnect")
# def handle_disconnect():
#     print("Client disconnected")
###############################################################################################


@app.route('/')
def hello():
    # print(os.getenv('JWT_KEY'))
    # print(len(os.getenv('JWT_KEY')))
    return 'Hello, World!'


############################# Utility Functions ##########################################

@app.route("/getFYList", methods=["GET"])
def getFYList():
    return getFinancialYearList(), 200


########################### Serving static files #########################################

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory("static/images", filename)

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory("static/files", filename)

############################ Login/ Register Operations ##################################


@app.route("/login", methods=["POST"])
def login():
    # print("here I am")
    user_id = request.json.get("email", None)
    password = request.json.get("password", None)
    # print(user_id, password)
    token = create_token(user_id, password)
    # print(token)
    return token


@app.route("/register", methods=["POST"])
def register():
    print("register")
    user_data = request.json
    registerRes = register_user(user_data)
    return registerRes


@app.route("/registerVerifyOTP", methods=["POST"])
def registerVerifyOTP():
    print("registerVerifyOTP")
    otp = request.json.get("otp")
    user_data = request.json.get("userData")
    registerVerifyRes = register_user_verify(otp, user_data)
    return registerVerifyRes


@app.route("/forgotPassword", methods=["POST"])
def forgotPassword():
    print("forgotPassword")
    user_data = request.json
    forgotPasswordRes = forgot_password(user_data)
    return forgotPasswordRes



@app.route("/forgotPasswordVerifyOTP", methods=["POST"])
def forgotPasswordVerifyOTP():
    print("forgotPasswordVerifyOTP")

    user_data = request.json

    forgotPasswordVerifyRes = forgot_password_verify(user_data)
    return forgotPasswordVerifyRes

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
@jwt_required()
def addStandardData():
    print("Adding/Updating Data")
    current_user = get_jwt_identity()

    product = request.json.get("product", None)
    uploadPoints = request.json.get("uploadPoints", {})
    files = request.json.get("files", None)
    targetTableClass = request.json.get("targetTableClass", None)
    # print(product)
    # print(uploadPoints)

    response = dataToStandardTable(current_user, product, uploadPoints, files, targetTableClass)
    
    return(response)

@app.route("/deleteStandardData", methods = ["GET","POST"])
@jwt_required()
def deleteStandardData():
    print("Deleting Data")
    current_user = get_jwt_identity()

    productIdToDelete = request.json.get("productIdToDelete", None)
    targetTableClass = request.json.get("targetTableClass", None)

    response = deleteFromStandardTable(current_user, productIdToDelete, targetTableClass)
    
    return response

@app.route("/downloadStandardData", methods = ["GET", "POST"])
@jwt_required(optional=True)
def downloadStandardData():
    print("Downloading Data")
    current_user = get_jwt_identity()

    productIdToDownload = request.json.get("productIdToDownload", None)
    targetTableClass = request.json.get("targetTableClass", None)

    response = downloadFromStandardTable(current_user, productIdToDownload, targetTableClass)
    
    return response


@app.route("/fetchAllStandardData", methods = ["GET","POST"])
@jwt_required(optional=True)
def fetchAllStandardData():
    print("Fetching Data")
    current_user = get_jwt_identity()

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

    response = fetchDataFromStandardTable(current_user, filterOptions, targetTableClass)
    
    return(response)


@app.route("/fetchStandardPageMetaData", methods = ["GET","POST"])
@jwt_required(optional=True)
def fetchStandardPageMetaData():
    current_user = get_jwt_identity()
    targetTableClass = request.json.get("targetTableClass", None)
   
    return fetchPageMetaData(current_user, targetTableClass)


########################################################################################

# main driver function
if __name__ == '__main__':

    # Run Migration only if a new Table is added.
    runMigration(app, db)
 
    app.run(debug = True, port = 4001, host = "0.0.0.0")
    # socketio.run(app, debug=True, port=4001, host="0.0.0.0")

