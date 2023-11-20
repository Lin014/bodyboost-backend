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
addUserRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
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
)
# responses: addFoodType
addUserResponses = {
    200: UsersSerializer,
    400: '{ "created": False, "message": "Duplicate account and/or password" } or ' + str(FormatErrorResponse('User'))
}

# request_body: updateUserPassword
updateUserPasswordRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'password': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User password'
        ),
    }
)
# responses: updateUserPassword
updateUserPasswordResponses = {
    200: UsersSerializer,
    400: '{ "message": "User cannot be changed." }',
    404: str(NotFoundResponse('User'))
}

# request_body: updateUserEmail
updateUserEmailRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User email'
        )
    }
)
# responses: updateUserEmail
updateUserEmailResponses = {
    200: UsersSerializer,
    400: '{ "message": "Duplicate email."}' + str(FormatErrorResponse('Email')) + ' or { "message": "User cannot be changed." }',
    404: str(NotFoundResponse('User'))
}

# responses: deleteUser
deleteUserResponses = {
    200: '{ "message": "User deleted successfully." }',
    404: str(NotFoundResponse('User'))
}

# request_body: login_normal
login_normalRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'account': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User account'
        ),
        'password': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User password'
        ),
    }
)
# responses: login_normal
login_normalResponses = {
    200: UsersSerializer,
    400: '{ "message": "Wrong password." }',
    404: str(NotFoundResponse('User'))
}

# request_body: login_google
login_googleRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User email'
        )
    }
)
# responses: login_google
login_googleResponses = {
    200: UsersSerializer,
    400: str(FormatErrorResponse('User'))
}
