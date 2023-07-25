from drf_yasg import openapi

from ..serializers import WeightHistorySerializer
from ..utils.response import *

# responses: getWeightHistoryByUserId
getWeightHistoryByUserIdResponses = {
    200: WeightHistorySerializer,
    404: str(NotFoundResponse('WeightHistory'))
}