# By default if a user has no entry, he/she will have ROLES.VIEWER

from .roles import Roles
USER_ROLES = {
    "00091" : [Roles.SUPER_ADMIN],
    "00339" : [Roles.SO_ADMIN],
<<<<<<< HEAD
    "00198" : [Roles.SO_ADMIN],
    "50088" : [Roles.SO_ADMIN],
    "00203" : [Roles.SO_ADMIN],
    "50039" : [Roles.SO_ADMIN],
    "50081" : [Roles.MO_ADMIN],
    "00082" : [Roles.MO_ADMIN],
    "60052" : [Roles.MO_ADMIN],
    "50082" : [Roles.MO_ADMIN],
    "00202" : [Roles.HR_ADMIN],
    "00022" : [Roles.HR_ADMIN],
    "00069" : [Roles.HR_ADMIN],
    "50054" : [Roles.CS_ADMIN],
    "00253" : [Roles.CS_ADMIN],
    "60025" : [Roles.CS_ADMIN],
    "00249" : [Roles.SCADA_ADMIN],
    "00261" : [Roles.SCADA_ADMIN],
=======
    "00198" : [Roles.SO_ADMIN,Roles.MO_ADMIN],
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
}