from drf_yasg import openapi

from ..serializers import AccuracySerializer
from ..utils.response import *

# responses: getAccuracyBySportRecordItemId
getAccuracyBySportRecordItemIdResponses = {
    200: AccuracySerializer,
    404: str(NotFoundResponse('Accuracy'))
}

# request_body: addAccuracy
addAccuracyRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'label': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='標籤名稱，如 up, down'
        ),
        'accuracy': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='準確率'
        ),
        'sport_record_item_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='id'
        ),
    }
)
# responses: addAccuracy
addAccuracyResponses = {
    200: AccuracySerializer,
    400: str(FormatErrorResponse('Accuracy')),
    404: str(NotFoundResponse('SportRecordItem'))
}

# responses: deleteAccuracy
deleteAccuracyResponses = {
    200: '{ "message": "Accuracy deleted successfully." }',
    404: str(NotFoundResponse('Accuracy'))
}