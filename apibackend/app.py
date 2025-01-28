from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from flask_cors import CORS
from datetime import timedelta


import os
from dotenv import load_dotenv

# Imports from other modules.
from auth import authentication


app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})

# Setup the Flask-JWT-Extended extension
load_dotenv(dotenv_path="../")
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)



@app.route('/')
def hello():
    print(os.getenv('JWT_KEY'))
    print(len(os.getenv('JWT_KEY')))
    return 'Hello, World!'

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