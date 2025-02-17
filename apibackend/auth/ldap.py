from ldap3 import Server, Connection, NTLM, ALL, SUBTREE
import os

def authenticate_ldap(username, password):

    LDAP_SERVER = os.getenv('LDAP_SERVER')
    LDAP_DOMAIN = os.getenv('LDAP_DOMAIN')  # Your AD domain
    LDAP_USER = f"{LDAP_DOMAIN}\\{username}"  # Format: DOMAIN\username
    BASE_DN = os.getenv('BASE_DN')  # Adjust this as per your AD structure
    
    try:
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
                    "eid":username,
                    "name": user_data.displayName.value if hasattr(user_data, "displayName") else None,
                    "email": user_data.mail.value if hasattr(user_data, "mail") else None,
                    "department": user_data.department.value if hasattr(user_data, "department") else None,
                    # "Title": user_data.title.value if hasattr(user_data, "title") else None,
                    # "User Principal Name": user_data.userPrincipalName.value if hasattr(user_data, "userPrincipalName") else None,
                    # "Groups": user_data.memberOf.values if hasattr(user_data, "memberOf") else None,
                    "Phone Number": user_data.telephoneNumber.value if hasattr(user_data, "telephoneNumber") else None,
                    "Mobile Number": user_data.mobile.value if hasattr(user_data, "mobile") else None,
                    "roles": [],
                    "organization": "ERLDC GRID-INDIA"
                }
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
        print(f"LDAP authentication error: {e}")
        return None
        # return False