from drf_yasg import openapi

from ..serializers import ProfileSerializer
from ..utils.response import *

# responses: getAllProfile
getAllProfileResponses = {
    200: ProfileSerializer,
    404: str(NotFoundResponse('Profile'))
}

# responses: getProfileById
getProfileByIdResponses = {
    200: ProfileSerializer,
    404: str(NotFoundResponse('Profile'))
}

# request_body: addProfile
addProfileRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='名字(暱稱)'
        ),
        'gender': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='性別 1:男生, 2:女生'
        ),
        'birthday': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='出生年月日, 格式: yyyy-mm-dd, 範例: 2023-05-23'
        ),
        'height': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='身高, 單位公分, 浮點數'
        ),
        'weight': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='體重, 單位公斤, 浮點數'
        ),
        'userID': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='相對應的user id, foreignkey'
        )
    }
)
# responses: addProfile
addProfileResponses = {
    200: ProfileSerializer,
    400: str(FormatErrorResponse('Profile')),
    404: str(NotFoundResponse('userID'))
}

# request_body: updateProfile
updateProfileRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='名字(暱稱)'
        ),
        'gender': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='性別 1:男生, 2:女生'
        ),
        'birthday': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='出生年月日, 格式: yyyy-mm-dd, 範例: 2023-05-23'
        ),
        'height': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='身高, 單位公分, 浮點數'
        ),
        'weight': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='體重, 單位公斤, 浮點數'
        ),
        'weight_goal': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='目標體重, 單位公斤, 浮點數'
        ),
        'goal': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='使用目標，health(維持身體健康), weight(減肥), muscle&fat(增肌減脂)'
        ),
        'body_fat': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='體脂率, 單位%, 浮點數'
        ),
    }
)
# responses: updateProfile
updateProfileResponses = {
    200: ProfileSerializer,
    400: str(FormatErrorResponse('Profile')),
    404: str(NotFoundResponse('Profile'))
}

# responses: deleteProfile
deleteProfileResponses = {
    200: '{ "message": "Profile deleted successfully." }',
    404: str(NotFoundResponse('Profile'))
}

# request_body: uploadProfileImage
uploadProfileImageRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['image'],
    properties={
        'image': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='上傳使用者大頭貼, 需將圖片轉為二進制',
            items=openapi.Items(type=openapi.TYPE_STRING)
        )
    }
)
# responses: uploadProfileImage
uploadProfileImageResponses = {
    200: ProfileSerializer,
    404: str(NotFoundResponse('Profile'))
}
