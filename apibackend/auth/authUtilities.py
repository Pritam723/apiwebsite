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