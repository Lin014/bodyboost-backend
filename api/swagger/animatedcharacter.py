from drf_yasg import openapi

from ..serializers import AnimationSerializer
from ..utils.response import *

# responses: getAnimation
getAnimationResponses = {
    200: AnimationSerializer,
    404: str(NotFoundResponse('Animation'))
}

# request_body: addAnimation
addAnimationRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='動畫人物的名字'
        ),
        'animation': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='上傳動畫影片',
            items=openapi.Items(type=openapi.TYPE_STRING)
        ),
        'image': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='上傳動畫縮圖照',
            items=openapi.Items(type=openapi.TYPE_STRING)
        ),
        'sport_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='運動項目 id'
        ),
    }
)
# responses: addAnimation
addAnimationResponses = {
    200: AnimationSerializer,
    400: str(FormatErrorResponse('Animation')) + 'or' + str(FormatErrorResponse("Animation's image")) + str(FormatErrorResponse("Animation's animation")),
    404: str(NotFoundResponse('User')) + 'or' + str(NotFoundResponse('Sport')) + 'or' + str(NotFoundResponse('SportGroupItem'))
}

# responses: deleteAnimation
deleteAnimationResponses = {
    200: '{"message": "Animation deleted successfully."}',
    404: str(NotFoundResponse('Animation'))
}