from drf_yasg import openapi

from ..serializers import BodyFatHistorySerializer
from ..utils.response import *

# responses: getBodyFatHistoryByUserId
getBodyFatHistoryByUserIdResponses = {
    200: BodyFatHistorySerializer,
    404: str(NotFoundResponse('BodyFatHistory'))
}

