from drf_yasg import openapi

from ..serializers import UserAchievementSerializer
from ..utils.response import *

# responses: getUserAchievementByUserId
getUserAchievementByUserIdResponses = {
    200: UserAchievementSerializer,
    404: str(NotFoundResponse('UserAchievement'))
}