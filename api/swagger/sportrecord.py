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
    404: str(NotFoundResponse('User')) + 'or' + str(NotFoundResponse('Sport')) + 'or' + str(NotFoundResponse('SportGroupItem'))
}

# request_body: updateSportRecordItem
updateSportRecordItemRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'completed_time': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='完成時間，格式： "yyyy-mm-dd hh:mm:ss'
        ),
        'time': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='運動做了多久'
        ),
        'counts': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='運動做的次數'
        ),
        'consumed_kcal': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='運動消耗的熱量'
        ),
    }
)
# responses: updateSportRecordItem
updateSportRecordItemResponses = {
    200: SportRecordItemSerializer,
    404: str(NotFoundResponse('SportRecordItem'))
}

# request_body: updateSportRecordItem
checkSportRequestBody = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    required=["completed_time", "time", "sport_record_id"],
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
            ),
            'completed_time': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'sport_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
            ),
            'custom_time': openapi.Schema(
                type=openapi.TYPE_NUMBER,
            ),
            'no': openapi.Schema(
                type=openapi.TYPE_INTEGER,
            ),
            'mode': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'time': openapi.Schema(
                type=openapi.TYPE_NUMBER,
            ),
            'counts': openapi.Schema(
                type=openapi.TYPE_INTEGER,
            ),
            'consumed_kcal': openapi.Schema(
                type=openapi.TYPE_NUMBER,
            ),
            'sport_record_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
            )
        }
    )
)

# responses: deleteSportRecord
deleteSportRecordResponses = {
    200: '{"message": "SportRecord deleted successfully."}',
    404: str(NotFoundResponse('SportRecord'))
}

# request_body: uploadSportRecordItemVideo
uploadSportRecordItemVideoRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['video'],
    properties={
        'video': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='上傳影片',
            items=openapi.Items(type=openapi.TYPE_STRING)
        )
    }
)
# responses: uploadSportRecordItemVideo
uploadSportRecordItemVideoResponses = {
    200: SportRecordItemSerializer,
    400: str(FormatErrorResponse('Video')),
    404: str(NotFoundResponse('SportRecordItem'))
}