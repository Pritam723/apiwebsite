# There are 2 special Roles.
# "ALL" which is applicable to pages only.
# "SUPER_ADMIN" which is applicable to users only.
# By default if a user has no entry in userRoles.py, he/she will have ROLES.VIEWER

from enum import Enum

class Roles(Enum):
    ALL = "ALL"
    VIEWER = "VIEWER"
    SO_ADMIN = "SO_ADMIN"
    SS_ADMIN = "SS_ADMIN"
    MO_ADMIN = "MO_ADMIN"
    SCADA_ADMIN = "SCADA_ADMIN"
    HR_ADMIN = "HR_ADMIN"
    PR_ADMIN = "PR_ADMIN"
    CS_ADMIN = "CS_ADMIN"
    IT_ADMIN = "IT_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

# # Accessing enum members using dot notation
# print(Roles.SO_ADMIN)       # Roles.SO_ADMIN

# # Getting the value of an enum member
# print(Roles.SO_ADMIN.value)  # "SO_ADMIN"

# # Getting the name of an enum member
# print(Roles.SO_ADMIN.name)   # "SO_ADMIN"