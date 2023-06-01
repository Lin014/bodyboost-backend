from drf_yasg import openapi

from ..serializers import EmailVerifyCode
from ..utils.response import *

# request_body: resendRegisterMail
resendRegisterMailRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'account': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User account'
        )
    }
)
# responses: resendRegisterMail
resendRegisterMailResponses = {
    200: '{ "message": "Send successfully.", "user": UsersObject }',
    404: str(NotFoundResponse('User'))
}

# request_body: sendForgetPasswordMail
sendForgetPasswordMailRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'account': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User account'
        )
    },
)
# responses: sendForgetPasswordMail
sendForgetPasswordMailResponses = {
    200: '{ "message": "Send successfully.", "user": UsersObject }',
    404: str(NotFoundResponse('User'))
}

# request_body: authenticationRegisterCode
authenticationRegisterCodeRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'code': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Register verification code.'
        ),
        'userID': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='User id.'
        )
    },
)
# responses: authenticationRegisterCode
authenticationRegisterCodeResponses = {
    200: '{ "message": "Verified successful.", "user": UserObject }',
    400: '{ "message": "Verified failed." } or { "message": "Verification code has expired." }',
    404: str(NotFoundResponse('EmailVerifyCode'))
}

# request_body: authenticationForgetPasswordCode
authenticationForgetPasswordCodeRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'code': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Register verification code.'
        ),
        'userID': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='User id.'
        )
    },
)
# responses: authenticationForgetPasswordCode
authenticationForgetPasswordCodeResponses = {
    200: '{ "message": "Verified successful." }',
    400: '{ "message": "Verified failed." } or { "message": "Verification code has expired." }',
    404: str(NotFoundResponse('EmailVerifyCode'))
}
