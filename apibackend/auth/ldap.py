from ldap3 import Server, Connection, NTLM, ALL, SUBTREE
import os
from .authUtilities import ResponseException
import re

def authenticate_ldap(username, password):

    try:
        LDAP_SERVER = os.getenv('LDAP_SERVER')
        LDAP_DOMAIN = os.getenv('LDAP_DOMAIN')  # Your AD domain
        LDAP_USER = f"{LDAP_DOMAIN}\\{username}"  # Format: DOMAIN\username
        BASE_DN = os.getenv('BASE_DN')  # Adjust this as per your AD structure
        

        # Define the LDAP server
        server = Server(LDAP_SERVER, get_info=ALL)
        
        # Try connecting with the provided credentials using NTLM
        conn = Connection(server, user=LDAP_USER, password=password, authentication=NTLM, auto_bind=True)

        if conn.bound:  # If authentication succeeds
            print("LDAP authentication successful!")
            
            # Search for user details
            search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
            conn.search(search_base=BASE_DN, search_filter=search_filter, search_scope=SUBTREE, attributes=[
                "cn", "displayName", "mail", "department", "title", "memberOf", "userPrincipalName", "telephoneNumber", "mobile"
            ])

            user_info = None

            if conn.entries:
                user_data = conn.entries[0]  # Get first search result
                user_info = {
                    "user_id": username,
                    # "eid":username,
                    "name": user_data.displayName.value if hasattr(user_data, "displayName") else None,
                    "email": user_data.mail.value if hasattr(user_data, "mail") else None,
                    # "department": user_data.department.value if hasattr(user_data, "department") else None,
                    # "Title": user_data.title.value if hasattr(user_data, "title") else None,
                    # "User Principal Name": user_data.userPrincipalName.value if hasattr(user_data, "userPrincipalName") else None,
                    # "Groups": user_data.memberOf.values if hasattr(user_data, "memberOf") else None,
                    "phoneNumber": user_data.telephoneNumber.value if hasattr(user_data, "telephoneNumber") else None,
                    "mobileNumber": user_data.mobile.value if hasattr(user_data, "mobile") else None,
                    "roles": [],
                    "organization": "ERLDC GRID-INDIA"
                }

                if(user_info["mobileNumber"] is None):
                    user_info["mobileNumber"] = user_info["phoneNumber"]
                # conn.unbind()
                # print(user_info)
            
            conn.unbind()
            return user_info
            # return True
        else:
            print("LDAP authentication failed!")
            return None
            # return False
    except Exception as e:
        print(e)
        return None

def isNotLDAPUser(identifier):  # Checks if this identifier is free in AD.



    LDAP_SERVER = os.getenv('LDAP_SERVER')
    BASE_DN = os.getenv('BASE_DN')  # Adjust this as per your AD structure
    SERVICE_ACCOUNT_USER = os.getenv('SERVICE_ACCOUNT_USER')  # Service account (replace with actual)
    SERVICE_ACCOUNT_PASSWORD = os.getenv('SERVICE_ACCOUNT_PASSWORD') # Service account password


   
    # Connect to LDAP server using a service account
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=SERVICE_ACCOUNT_USER, password=SERVICE_ACCOUNT_PASSWORD, authentication=NTLM, auto_bind=True)

    if conn.bound:  # If connection is successful
        print("Connected to LDAP successfully!")

        # Determine whether input is an email or username
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):  # Simple email regex check
            search_filter = f"(&(objectClass=user)(mail={identifier}))"
        else:
            search_filter = f"(&(objectClass=user)(sAMAccountName={identifier}))"

        # Search for the identifier
        conn.search(
            search_base=BASE_DN,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=["cn", "sAMAccountName", "mail"]
        )

        if conn.entries:
            user_data = conn.entries[0]  # Get first search result
            user_info = {
                "Full Name": user_data.cn.value if hasattr(user_data, "cn") else None,
                "Username": user_data.sAMAccountName.value if hasattr(user_data, "sAMAccountName") else None,
                "Email": user_data.mail.value if hasattr(user_data, "mail") else None,
            }
            print(f"Found in Active Directory: {user_info}")
            conn.unbind()
            return False # Means the user is in LDAP.
        else:
            print(f"{identifier} does NOT exist in Active Directory!")
            conn.unbind()
            return True

    else:
        print("Failed to connect to LDAP!")
        return True # Returning True is safe.