from drf_yasg import openapi

from ..serializers import GoalHistorySerializer
from ..utils.response import *

# responses: getGoalHistoryByUserId
getGoalHistoryByUserIdResponses = {
    200: GoalHistorySerializer,
    404: str(NotFoundResponse('GoalHistory'))
}