# By default if a user has no entry, he/she will have ROLES.VIEWER

from .roles import Roles
USER_ROLES = {
    "00091" : [Roles.SUPER_ADMIN],
    "00339" : [Roles.SO_ADMIN],
    "00198" : [Roles.SO_ADMIN]
}