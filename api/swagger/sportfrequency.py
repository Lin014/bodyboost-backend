from drf_yasg import openapi

from ..serializers import SportFrequencySerializer
from ..utils.response import *

# responses: getAllSportFrequency
getAllSportFrequencyResponses = {
    200: SportFrequencySerializer,
    404: str(NotFoundResponse('SportFrequency'))
}

# request_body: addSportFrequency
addSportFrequencyRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sport_id': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='運動項目 id'
        ),
    }
)
# responses: addSportFrequency
addSportFrequencyResponses = {
    200: "{ 'message': 'Add Successfully.'}",
    400: str(FormatErrorResponse('SportFrequency')),
    404: str(NotFoundResponse('Sport'))
}

# responses: deleteSportFrequency
deleteSportFrequencyResponses = {
    200: '{"message": "SportFrequency deleted successfully."}',
    404: str(NotFoundResponse('SportFrequency'))
}