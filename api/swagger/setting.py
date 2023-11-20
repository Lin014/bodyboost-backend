from drf_yasg import openapi

from ..serializers import SettingSerializer
from ..utils.response import *

# responses: getSettingByUserId
getSettingByUserIdResponses = {
    200: SettingSerializer,
    404: str(NotFoundResponse('Setting'))
}

# request_body: updateSetting
updateSettingRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'theme': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='主題，ligth, dark'
        ),
        'anim_char_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='動畫人物的名字'
        ),
        'is_alerted': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='是否要通知運動時間'
        ),
        'alert_day': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='is_alerted等於true才需要填，星期幾，可複選, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday',
            items=openapi.Items(type=openapi.TYPE_STRING)
        ),
        'alert_time': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='is_alerted等於true才需要填，格式: hh:mm:ss, 範例: 12:00:00'
        ),
    }
)
# responses: updateSetting
updateSettingResponses = {
    200: SettingSerializer,
    400: str(FormatErrorResponse('Setting')),
    404: str(NotFoundResponse('Animation'))
}