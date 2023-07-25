from drf_yasg import openapi

from ..serializers import NotificationHistorySerializer
from ..utils.response import *

# responses: getNotificationHistoryByUserId
getNotificationHistoryByUserIdResponses = {
    200: NotificationHistorySerializer,
    404: str(NotFoundResponse('NotificationHistory'))
}


# request_body: addNotificationHistory
addNotificationHistoryRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='通知內容'
        ),
        'is_read': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='是否已讀過，如果不填，預設是 false'
        ),
        'label': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='標籤分類'
        ),
        'create_at': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='時間，預設是添加現在時間，也可自行輸入，格式："2023-07-25 16:00:00"'
        ),
        'user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='user id'
        ),
    }
)
# responses: addNotificationHistory
addNotificationHistoryResponses = {
    200: NotificationHistorySerializer,
    400: str(FormatErrorResponse('NotificationHistory')),
    404: str(NotFoundResponse('User'))
}

# responses: deleteNotificationHistory
deleteNotificationHistoryResponses = {
    200: '{ "message": "NotificationHistory deleted successfully." }',
    404: str(NotFoundResponse('NotificationHistory'))
}