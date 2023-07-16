from drf_yasg import openapi

from ..serializers import SportSerializer
from ..utils.response import *

# responses: getAllSport
getAllSportResponses = {
    200: SportSerializer,
    404: str(NotFoundResponse('Sport'))
}

# responses: getSportById
getSportByIdResponses = {
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