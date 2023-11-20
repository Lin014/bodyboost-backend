from drf_yasg import openapi

from ..serializers import WaterHistorySerializer
from ..utils.response import *

# responses: getWaterHistoryByUserId
getWaterHistoryByUserIdResponses = {
    200: WaterHistorySerializer,
    404: str(NotFoundResponse('WaterHistory'))
}

# request_body: addWaterHistory
addWaterHistoryRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'water': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='飲水量，單位 ml'
        ),
        'user_id': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='user id'
        ),
        'date': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='飲水時間，格式: yyyy-mm-dd hh:mm:ss, 範例: 2023-05-23 12:00:00'
        )
    }
)
# responses: addWaterHistory
addWaterHistoryResponses = {
    200: WaterHistorySerializer,
    400: str(FormatErrorResponse('WaterHistory')),
    404: str(NotFoundResponse('User'))
}

# responses: deleteWaterHistory
deleteWaterHistoryResponses = {
    200: '{ "message": "WaterHistory deleted successfully." }',
    404: str(NotFoundResponse('WaterHistory'))
}