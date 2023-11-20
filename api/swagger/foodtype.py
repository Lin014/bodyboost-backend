from drf_yasg import openapi

from ..serializers import FoodTypeSerializer
from ..utils.response import *

# responses: getAllFoodType
getAllFoodTypeResponses = {
    200: FoodTypeSerializer,
    404: str(NotFoundResponse('FoodType'))
}

# request_body: addFoodType
addFoodTypeRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='食物類別'
        )
    }
)

# responses: addFoodType
addFoodTypeResponses = {
    200: FoodTypeSerializer,
    400: '{ "message": "FoodType already exists.", "foodType": FoodTypeObject }'
}

# request_body: updateFoodType
updateFoodTypeRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='食物類別'
        ),
    }
)

# responses: updateFoodType
updateFoodTypeResponses = {
    200: FoodTypeSerializer,
    404: str(NotFoundResponse('FoodType'))
}

# responses: deleteFoodType
deleteFoodTypeResponses = {
    200: '{ "message": "FoodType deleted successfully." }',
    404: str(NotFoundResponse('FoodType'))
}
