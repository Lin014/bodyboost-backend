from drf_yasg import openapi

from ..serializers import CustomFoodSerializer
from ..utils.response import *

# responses: getAllCustomFood
getAllCustomFoodResponses = {
    200: CustomFoodSerializer,
    404: str(NotFoundResponse('CustomFood'))
}

# request_body: addCustomFood
addCustomFoodRequestBody = openapi.Schema(
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
        'user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='創建者id'
        )
    }
)
# responses: addCustomFood
addCustomFoodResponses = {
    200: CustomFoodSerializer,
    400: str(FormatErrorResponse('CustomFood'))
}

# request_body: updateCustomFood
updateCustomFoodRequestBody = openapi.Schema(
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
        'food_type_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='食物類型關聯id'
        ),
        'store_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='所屬商店關聯id'
        )
    }
)
# responses: updateCustomFood
updateCustomFoodResponses = {
    200: CustomFoodSerializer,
    400: str(FormatErrorResponse('CustomFood')),
    404: str(NotFoundResponse('CustomFood'))
}

# responses: deleteCustomFood
deleteCustomFoodResponses = {
    200: '{ "message": "Custom Food deleted successfully." }',
    404: str(NotFoundResponse('CustomFood'))
}