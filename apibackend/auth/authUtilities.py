import re
import random

class ResponseException(Exception):
    pass

def getPermissionFlags(allowedReadRoles, allowedWriteRoles, user_info):
    
    # user_info = {'user_id': '00091', 'department': 'IT', 'eid': '00091', 'name': 'Pritam Dutta', 
    #  'email': 'pritam.dutta@grid-india.in', 'organization': 'ERLDC GRID-INDIA', 'roles': ['SO_ADMIN', 'IT_ADMIN']}
    readPermission = False
    writePermission = False

    userRoles = user_info.get("roles", [])

    if(len(set(userRoles) & set(allowedReadRoles))):
        readPermission = True
    if(len(set(userRoles) & set(allowedWriteRoles))):
        writePermission = True
        
    if(("ALL" in allowedReadRoles) or ("SUPER_ADMIN" in userRoles)):
        readPermission = True
    if(("ALL" in allowedWriteRoles) or ("SUPER_ADMIN" in userRoles)):
        writePermission = True

    return readPermission, writePermission


def is_valid_password(password):
    """Check if password meets complexity requirements."""
    if (len(password) < 8 or
        not re.search(r'[a-z]', password) or  # At least one lowercase
        not re.search(r'[A-Z]', password) or  # At least one uppercase
        not re.search(r'\d', password)):     # At least one numeric
        return False
    return True



def generate_validation_code():
    """Generate a random 6-digit code that is not all zeros."""
    while True:
        code = str(random.randint(100000, 999999))  # Ensures a 6-digit number
        if code != "000000":  # Extra safety check
            return code


