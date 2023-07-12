from drf_yasg import openapi

from ..serializers import DailyBonusSerializer
from ..utils.response import *

# responses: getDailyBonusById
getDailyBonusByIdResponses = {
    200: DailyBonusSerializer,
    404: str(NotFoundResponse('DailyBonus'))
}

# responses: addDailyBonusById
addDailyBonusByIdResponses = {
    200: DailyBonusSerializer,
    404: str(NotFoundResponse('User')),
    400: str(FormatErrorResponse('DailyBonus'))
}

