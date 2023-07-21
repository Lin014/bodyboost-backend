from drf_yasg import openapi

from ..serializers import SportRecordSerializer, SportRecordItemSerializer
from ..utils.response import *

# responses: getSportRecordByUserId
getSportRecordByUserIdResponses = {
    200: SportRecordSerializer,
    404: str(NotFoundResponse('SportRecord'))
}

# request_body: addSportRecord
addSportRecordRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='運動類型，single, combo'
        ),
        'is_record_video': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='是否錄影'
        ),
        'user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='User id'
        ),
        'sport_group_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='如果type是combo才需要填，SportGroup id'
        ),
        'sport_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='如果type是single才需要填，Sport id'
        ),
        'mode': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='如果type是single才需要填，timing, counting, none'
        ),
        'custom_time': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='如果type是single而且是計時模式才需要填，填入使用者輸入的時間'
        ),
        'custom_counts': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='如果type是single而且是計次模式才需要填，填入使用者輸入的次數'
        ),
    }
)
# responses: addSportRecord
addSportRecordResponses = {
    200: SportRecordSerializer,
    400: str(FormatErrorResponse('SportRecord')) + 'or' + str(FormatErrorResponse('SportRecordItem')),
    404: str(NotFoundResponse('User'))
}

# responses: deleteSportRecord
deleteSportRecordResponses = {
    200: '{"message": "SportRecord deleted successfully."}',
    404: str(NotFoundResponse('SportRecord'))
}