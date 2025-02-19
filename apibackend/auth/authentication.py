from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


from datetime import datetime, timedelta


from .authUtilities import ResponseException, is_valid_password, generate_validation_code
from .ldap import authenticate_ldap, isNotLDAPUser
from models.models import db, User

import os

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
def create_token(user_id, password):
    try: 
        # m = 0/0 # Generating Error.
        print("Checking LDAP")
        user_data = None

        user_data = authenticate_ldap(user_id, password)

        if(user_data is None):
            print("Checking DB")
            # Check DB.
            # Fetch user from the database
            user = User.query.filter_by(userId=user_id).first()

            # Check if user exists and verify password

            salted_password = os.getenv('PASSWORD_SALT') + password

            if user and user.isValidated and check_password_hash(user.password, salted_password):
                user_data = {}
                user_data["user_id"] = user.userId
                user_data["name"] = user.name
                user_data["email"] = user.email
                user_data["organization"] = user.organization
                user_data["mobileNumber"] = user.mobileNumber
     
        if(user_data is None):
            raise ResponseException({"message" : "Incorrect username or password.", "summary" : "Incorrect username or password.", "status" : 401})

        user_data["roles"] =  ["SO_ADMIN", "IT_ADMIN"] # Change this later.


        customIdentity = user_id
        # additional_claims = {"aud": "some_audience", "foo": "bar"}
        # user_data = {"user_id": user_id, "name" : "Pritam Dutta", "mobileNumber": "8981224244"
        #              "email" : "pritam.dutta@grid-india.in", "organization" : "ERLDC GRID-INDIA", "roles" : ["SO_ADMIN", "IT_ADMIN"]}

            
        additional_claims = {"user_info" : user_data}

        access_token = create_access_token(identity=customIdentity, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=customIdentity)

        # payload = get_jwt_identity()
        # print(payload)

        # return jsonify(access_token=access_token, refresh_token=refresh_token), 200

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        jsonData = {
            "success": True,
            "summary":"Login Successful",
            "message": "Login Successful.",
            "data": data,
            "type": "success"
        }

        # print("Works here")

        return jsonify(jsonData), 200

    
    except ResponseException as e:
  
        error_dict = e.args[0]
        print(error_dict)
        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]
    
    except Exception as e:

        print(e)
        print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


def register_user(user_data):
    try:
        # m = 0/0
        # print(user_data)
        # {'name': 'Pritam Dutta', 'email': 'pritam.dutta@grid-india.in', 'organization': 'Grid Controller of India LTD', 
        #  'mobilenumber': '8981224244', 'password': 'Posoco@123', 'confirmPassword': 'Posoco@123'}

        timeNow = datetime.today()

        # Now check the User Table.
        email = user_data.get('email')
        name = user_data.get('name')
        organization = user_data.get('organization')
        mobile_number = user_data.get('mobilenumber')  # Ensure the key matches
        password = user_data.get('password')
        confirm_password = user_data.get('confirmPassword')

        if(not isNotLDAPUser(email)):
            raise ResponseException({"message" : "User already exists!!", "summary" : "User already exists", "status" : 500})

        email_alt = None
        if "posoco.in" in email:
            email_alt = email.replace("posoco.in", "grid-india.in")
        if "grid-india.in" in email:
            email_alt = email.replace("grid-india.in","posoco.in")
            
        if(email_alt and (not isNotLDAPUser(email_alt))):
            raise ResponseException({"message" : "User already exists!!", "summary" : "User already exists", "status" : 500})



        if(not is_valid_password(password)):
            raise ResponseException({"message" : "Password does not meet minimum complexity", "summary" : "Password does not meet minimum complexity", "status" : 500})


        # Check if email already exists
        existing_user = User.query.filter_by(userId=email).first()
        if(existing_user and existing_user.isValidated == True):
            raise ResponseException({"message" : "User already exists!!", "summary" :"User already exists!!", "status" : 400})

        if(existing_user and existing_user.isValidated == False):
            # So, user exists but not validated. So just delete it and enter new user again.
            db.session.delete(existing_user)  # Delete user from database
            db.session.commit()  # Save changes


        # Validate password confirmation
        if password != confirm_password:
            raise ResponseException({"message" : "Both the Passwords do not match!!", "summary" :"Both the Passwords do not match!!", "status" : 400})

        salted_password = os.getenv('PASSWORD_SALT') + password
        # Hash the password before storing
        hashed_password = generate_password_hash(salted_password)

        # Create new user object

        randomCode = generate_validation_code()

        new_user = User(
            userId=email,  # Using email as primary key
            name=name,
            email=email,
            organization=organization,
            mobileNumber=mobile_number,
            password=hashed_password,
            userCreatedOn=timeNow,
            lastModifiedOn=timeNow,
            isDeleted=False,
            isValidated=False,
            validationCode=randomCode,
            codeValidity = timeNow + timedelta(minutes = 5)
        )

        # Save to database
        db.session.add(new_user)
        db.session.commit()


        data = {
            "info": f"User registered successfully with UserID/EmailID: {email}"
        }

        jsonData = {
            "success": True,
            "summary":"User registered successfully",
            "message": "User registered successfully.",
            "data": data,
            "type": "success"
        }

        # print("Works here")

        return jsonify(jsonData), 200
    
    except ResponseException as e:
  
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]
    
    except Exception as e:

        print(e)
        print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500


def register_user_verify(otp, user_data):
    
    try:
        # print(otp)
        # print(user_data)
        timeNow = datetime.today()


        # Now check the User Table.
        email = user_data.get('email')
        password = user_data.get('password')


        # Fetch user from the database
        user = User.query.filter_by(userId=email).first()

        # Check if user exists and verify password
        salted_password = os.getenv('PASSWORD_SALT') + password
        if not user or not check_password_hash(user.password, salted_password):
            raise ResponseException({"message" : "Your user could not be verified!!", "summary" :"Your user could not be verified!!", "status" : 400})

        if user.isValidated:
            raise ResponseException({"message" : "User is already verified!!", "summary" :"User is already verified!!", "status" : 400})

        db_time_naive = user.codeValidity.replace(tzinfo=None)
        # print(db_time_naive)
        # print(timeNow)
        if(timeNow > db_time_naive):
            raise ResponseException({"message" : "Your OTP has expired!!", "summary" :"Your OTP has expired!!", "status" : 400})

        if(user.validationCode == "000000"):
            raise ResponseException({"message" : "OTP does not match!!", "summary" :"OTP does not match!!", "status" : 400})

        if(otp != user.validationCode):
            raise ResponseException({"message" : "OTP does not match!!", "summary" :"OTP does not match!!", "status" : 400})

        # We are here means it is a match. User is verified.
        user.isValidated = True
        user.validationCode = "000000"

        # Commit changes to database
        db.session.commit()

        data = {
            "info": f"User verified successfully with UserID/EmailID: {email}"
        }

        jsonData = {
            "success": True,
            "summary":"User registered & verified successfully",
            "message": "User registered & verified successfully.",
            "data": data,
            "type": "success"
        }

        # print("Works here")

        return jsonify(jsonData), 200
    
    except ResponseException as e:
  
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]
    
    except Exception as e:

        print(e)
        print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500

def forgot_password(user_data):
    try:
        timeNow = datetime.today()

        # print(user_data)
        email = user_data.get('email')
        # print(email)

        if(not isNotLDAPUser(email)):
            raise ResponseException({"message" : "ERLDC users may contact local IT administrator to change Password!!", 
                                     "summary" : "ERLDC users may contact local IT administrator to change Password!!", "status" : 500})


        email_alt = None
        if "posoco.in" in email:
            email_alt = email.replace("posoco.in", "grid-india.in")
        if "grid-india.in" in email:
            email_alt = email.replace("grid-india.in","posoco.in")
            
        if(email_alt and (not isNotLDAPUser(email_alt))):
            raise ResponseException({"message" : "Please Contact Local IT Administrator!!", 
                                     "summary" : "ERLDC users may contact local IT administrator to change Password!!", "status" : 500})

        # Now we go to DB.
        # Check if email already exists
        existing_user = User.query.filter_by(userId=email).first()
        if(not (existing_user and existing_user.isValidated == True)):
            raise ResponseException({"message" : "No user Found!!", "summary" :"No user Found!!", "status" : 400})
        
        randomCode = generate_validation_code()

        # We are here means it is a match. User is verified.
        existing_user.validationCode = randomCode
        existing_user.codeValidity = timeNow + timedelta(minutes=5)
        
        # Commit changes to database
        db.session.commit()

        
        data = {
            "info": f"OTP has been sent to: {email}"
        }

        jsonData = {
            "success": True,
            "summary":"OTP Sent",
            "message": "OTP Sent.",
            "data": data,
            "type": "success"
        }

        # print("Works here")

        return jsonify(jsonData), 200


    except ResponseException as e:
  
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]
    
    except Exception as e:

        print(e)
        print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500
    
def forgot_password_verify(user_data):
    try:
        timeNow = datetime.today()

        print(user_data)
        email = user_data.get('email')
        otp = user_data.get('otp')
        newPassword = user_data.get('newPassword')
        confirmPassword = user_data.get('confirmPassword')
        
        print(email, otp, newPassword, confirmPassword)

        if(not is_valid_password(newPassword)):
            raise ResponseException({"message" : "Password does not meet minimum complexity", "summary" : "Password does not meet minimum complexity", "status" : 500})
       # Validate password confirmation
        if newPassword != confirmPassword:
            raise ResponseException({"message" : "Both the Passwords do not match!!", "summary" :"Both the Passwords do not match!!", "status" : 400})


        # Now we go to DB.
        # Check if email already exists
        existing_user = User.query.filter_by(userId=email).first()
        if(not (existing_user and existing_user.isValidated == True)):
            raise ResponseException({"message" : "No user Found!!", "summary" :"No user Found!!", "status" : 400})
        
        # We are here means it is a match. User is verified.

 
        salted_password = os.getenv('PASSWORD_SALT') + newPassword
        # Hash the password before storing
        hashed_password = generate_password_hash(salted_password)


        db_time_naive = existing_user.codeValidity.replace(tzinfo=None)
        # print(db_time_naive)
        # print(timeNow)
        if(timeNow > db_time_naive):
            raise ResponseException({"message" : "Your OTP has expired!!", "summary" :"Your OTP has expired!!", "status" : 400})

        if(existing_user.validationCode == "000000"):
            raise ResponseException({"message" : "OTP does not match!!", "summary" :"OTP does not match!!", "status" : 400})

        if(otp != existing_user.validationCode):
            raise ResponseException({"message" : "OTP does not match!!", "summary" :"OTP does not match!!", "status" : 400})

        # We are here means it is a match. User is verified.
        existing_user.validationCode = "000000"
        existing_user.password = hashed_password
        # Commit changes to database
        db.session.commit()

        
        data = {
            "info": f"Password Changed for the Mail ID: {email}"
        }

        jsonData = {
            "success": True,
            "summary":"Password Changed successfully",
            "message": "Password Changed successfully.",
            "data": data,
            "type": "success"
        }

        # print("Works here")

        return jsonify(jsonData), 200









    except ResponseException as e:
  
        error_dict = e.args[0]

        jsonData = {
            "success": False,
            "type": "error",
            "summary": error_dict["summary"],
            "message": error_dict["message"],
            "error": error_dict["message"]
        }

        return jsonify(jsonData), error_dict["status"]
    
    except Exception as e:

        print(e)
        print(str(e))

        jsonData = {
            "success": False,
            "type": "error",
            "summary": "Something went wrong",
            "message": str(e),
            "error": "Unknown Exception. Something went wrong"
        }

        return jsonify(jsonData), 500

# # Protect a route with jwt_required, which will kick out requests
# # without a valid JWT present.
# # @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200