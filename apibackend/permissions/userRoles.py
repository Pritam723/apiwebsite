# By default if a user has no entry, he/she will have ROLES.VIEWER

from .roles import Roles
USER_ROLES = {
    "00091" : [Roles.SUPER_ADMIN],
    "00339" : [Roles.SUPER_ADMIN],
    "00198" : [Roles.SUPER_ADMIN],
    "50088" : [Roles.SO_ADMIN],
    "00203" : [Roles.SO_ADMIN],
    "50039" : [Roles.SO_ADMIN],
    "00300" : [Roles.SO_ADMIN],
    "00221" : [Roles.SO_ADMIN],
    "50081" : [Roles.MO_ADMIN],
    "00082" : [Roles.MO_ADMIN],
    "60052" : [Roles.MO_ADMIN],
    "50082" : [Roles.MO_ADMIN],
    "00284" : [Roles.MO_ADMIN],
    "00296" : [Roles.MO_ADMIN],
    "60028" : [Roles.MO_ADMIN],
    "00264" : [Roles.MO_ADMIN],
    "00202" : [Roles.HR_ADMIN],
    "00022" : [Roles.HR_ADMIN],
    "00069" : [Roles.HR_ADMIN],
    "50054" : [Roles.CS_ADMIN],
    "00253" : [Roles.CS_ADMIN],
    "60025" : [Roles.CS_ADMIN],
    "00249" : [Roles.SCADA_ADMIN],
    "00261" : [Roles.SCADA_ADMIN],
    "00277" : [Roles.SCADA_ADMIN],
    "rtsd" : [Roles.SO_ADMIN],
    "RTSD" : [Roles.SO_ADMIN],
    "00218" : [Roles.MO_ADMIN]
}