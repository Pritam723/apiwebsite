from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
def create_token(user_id, password):
    if user_id != "00091" or password != "00091":
        print("No user matches. Returning 401")
        return jsonify({"msg": "Bad username or password"}), 401

    customIdentity = {"user_id": user_id, "department": "IT", "eid" : "00091", "name" : "Pritam"}
    # additional_claims = {"aud": "some_audience", "foo": "bar"}
    additional_claims = {}
    access_token = create_access_token(identity=customIdentity, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=customIdentity)

    # payload = get_jwt_identity()
    # print(payload)


    return jsonify(access_token=access_token, refresh_token=refresh_token)


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
# @app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200