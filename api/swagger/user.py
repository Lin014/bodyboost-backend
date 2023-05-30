from drf_yasg import openapi

from ..serializers import UsersSerializer
from ..utils.response import *

# responses: getAllUser
getAllUserResponses = {
    200: UsersSerializer,
    404: str(NotFoundResponse('User'))
}

# responses: getUserById
getUserByIdResponses = {
    200: UsersSerializer,
    404: str(NotFoundResponse('User'))
}

# request_body: addUser
addUserRequestBody = {
    'account': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User account'
    ),
    'password': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User password'
    ),
    'email': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User email'
    ),
}
# responses: addFoodType
addUserResponses = {
    200: UsersSerializer,
    400: '{ "created": False, "message": "Duplicate account and/or password" } or ' + str(FormatErrorResponse('User'))
}

# request_body: updateUser
updateUserRequestBody = {
    'password': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User password'
    ),
    'email': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User email'
    )
}
# responses: updateUser
updateUserResponses = {
    200: UsersSerializer,
    400: str(FormatErrorResponse('Email')) + ' or { "message": "User cannot be changed." }',
    404: str(NotFoundResponse('User'))
}

# responses: deleteUser
deleteUserResponses = {
    200: '{ "message": "User deleted successfully." }',
    404: str(NotFoundResponse('User'))
}

# request_body: login_normal
login_normalRequestBody = {
    'account': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User account'
    ),
    'password': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User password'
    ),
}
# responses: login_normal
login_normalResponses = {
    200: UsersSerializer,
    400: '{ "message": "Wrong password." }',
    404: str(NotFoundResponse('User'))
}

# request_body: login_google
login_googleRequestBody = {
    'email': openapi.Schema(
        type=openapi.TYPE_STRING,
        description='User email'
    )
}
# responses: login_google
login_googleResponses = {
    200: UsersSerializer,
    400: str(FormatErrorResponse('User'))
}
