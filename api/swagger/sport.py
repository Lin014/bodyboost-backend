from drf_yasg import openapi

from ..serializers import SportSerializer
from ..utils.response import *

# responses: getAllSportByUserIdSport
getAllSportByUserIdResponses = {
    200: SportSerializer,
    404: str(NotFoundResponse('Sport'))
}

# request_body: getSportByIdAndUserId
getSportByIdAndUserIdRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sport_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='運動項目 id'
        ),
        'user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='使用者 id'
        ),
    }
)
# responses: getSportByIdAndUserId
getSportByIdAndUserIdResponses = {
    200: SportSerializer,
    404: str(NotFoundResponse('Sport'))
}

# request_body: addSport
addSportRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='運動名稱'
        ),
        'description': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='運動描述'
        ),
        'default_time': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='運動預設時間'
        ),
        'interval': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='運動循環一次時長'
        ),
        'is_count': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='可否計數'
        ),
        'met': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='MET'
        ),
        'type': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='有氧(aerobics)、無氧(anaerobic)運動'
        ),
    }
)
# responses: addSport
addSportResponses = {
    200: SportSerializer,
    400: str(FormatErrorResponse('Sport'))
}

# responses: updateSport
updateSportResponses = {
    200: SportSerializer,
    404: str(NotFoundResponse('Sport'))
}

# responses: deleteSport
deleteSportResponses = {
    200: '{"message": "Sport deleted successfully."}',
    404: str(NotFoundResponse('Sport'))
}