from drf_yasg import openapi

from ..serializers import SportGroupSerializer, SportGroupItemSerializer
from ..utils.response import *

# responses: getSportGroupByUserId
getSportGroupByUserIdResponses = {
    200: SportGroupSerializer,
    404: str(NotFoundResponse('SportGroup'))
}

# request_body: addSportGroup
addSportGroupRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='運動組合名稱'
        ),
        'rest_time': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='運動組合間隔/休息時間'
        ),
        'user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='user id'
        ),
        'items': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='所有 SportGroupItem',
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'no': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='順序編號'
                    ),
                    'mode': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='timing, counting , none'
                    ),
                    'custom_time': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description='使用者自訂時間'
                    ),
                    'custom_counts': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='使用者自訂次數'
                    ),
                    'sport_id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Sport id'
                    ),
                }
            )
        ),
    }
)
# responses: addSportGroup
addSportGroupResponses = {
    200: SportGroupSerializer,
    400: str(FormatErrorResponse('SportGroup')) + 'or' + str(FormatErrorResponse('SportGroupItem')),
    404: str(NotFoundResponse('User'))
}

# responses: updateSportGroup
updateSportGroupResponses = {
    200: SportGroupSerializer,
    400: str(FormatErrorResponse('SportGroupItem')),
    404: str(NotFoundResponse('SportGroup'))
}

# request_body: updateOnlySportGroup
updateOnlySportGroupRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='運動組合名稱'
        ),
        'rest_time': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='運動組合間隔/休息時間'
        ),
        'user_id': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='user id'
        ),
    }
)
# responses: updateOnlySportGroup
updateOnlySportGroupResponses = {
    200: SportGroupSerializer,
    404: str(NotFoundResponse('SportGroup'))
}

# responses: deleteSportGroup
deleteSportGroupResponses = {
    200: '{"message": "SportGroup deleted successfully."}',
    404: str(NotFoundResponse('SportGroup'))
}