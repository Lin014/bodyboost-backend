from drf_yasg import openapi

from ..serializers import UserAchievementSerializer
from ..utils.response import *

# responses: getUserAchievementByUserId
getUserAchievementByUserIdResponses = {
    200: UserAchievementSerializer,
    404: str(NotFoundResponse('UserAchievement'))
}

# request_body: updateUserAchievement
updateUserAchievementRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'is_achieve': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='是否達成成就'
        )
    }
)