from drf_yasg import openapi

from ..serializers import FoodSerializer
from ..utils.response import *
from .page import pageManualParameters

nameManualParameters = [
    openapi.Parameter(
        name='name',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='查詢關鍵字',
        required=True
    ),
    *pageManualParameters,
]

# responses: getAllFood
getAllFoodResponses = {
    200: FoodSerializer,
    404: str(NotFoundResponse('Food'))
}

# responses: getFoodByName
getFoodByNameResponses = {
    200: FoodSerializer,
    400: str({'message': 'Please provide a name parameter'}),
    404: str(NotFoundResponse('Food'))
}

# request_body: addFood
addFoodRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='名稱'
        ),
        'calorie': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='熱量，浮點數型態'
        ),
        'size': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='體積或容量'
        ),
        'unit': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='單位，通常為g或ml'
        ),
        'protein': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='蛋白質，浮點數型態'
        ),
        'fat': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='脂肪，浮點數型態'
        ),
        'carb': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='碳水化合物，浮點數型態'
        ),
        'sodium': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='鈉，浮點數型態'
        ),
        'modify': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='可調整克數與不可調整克數，True or False'
        ),
        'food_type_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='食物類型關聯id'
        ),
        'store_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='所屬商店關聯id'
        ),
    }
)
# responses: addFood
addFoodResponses = {
    200: FoodSerializer,
    400: str(FormatErrorResponse('Food'))
}

# responses: updateFood
updateFoodResponses = {
    200: FoodSerializer,
    400: str(FormatErrorResponse('Food')),
    404: str(NotFoundResponse('Food'))
}

# responses: deleteFood
deleteFoodResponses = {
    200: '{ "message": "Food deleted successfully." }',
    404: str(NotFoundResponse('Food'))
}