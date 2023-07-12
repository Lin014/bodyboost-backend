from drf_yasg import openapi

from ..serializers import DietRecordSerializer
from ..utils.response import *

# responses: getAllDietRecord
getAllDietRecordResponses = {
    200: DietRecordSerializer,
    404: str(NotFoundResponse('DietRecord'))
}

# request_body: addDietRecord
addDietRecordRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'date': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='食用日期，格式: yyyy-mm-dd, 範例: 2023-05-23'
        ),
        'serving_amount': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description='食用量，體積或容量'
        ),
        'label': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='標籤，例如：早餐、早午餐、午餐、晚餐'
        ),
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
            description='所屬使用者id'
        ),
    }
)
# responses: addDietRecord
addDietRecordResponses = {
    200: DietRecordSerializer,
    400: str(FormatErrorResponse('DietRecord'))
}

# responses: updateDietRecord
updateDietRecordResponses = {
    200: DietRecordSerializer,
    404: str(NotFoundResponse('DietRecord'))
}