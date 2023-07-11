from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import DietRecord, Users, FoodType, Store
from ..serializers import DietRecordSerializer
from ..utils.response import *
from ..swagger.dietrecord import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["DietRecord"],
    operation_summary='查詢全部飲食紀錄',
    operation_description="",
    responses=getAllDietRecordResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllDietRecord(request):
    all_food = DietRecord.objects.all()
    serializer = DietRecordSerializer(all_food, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('DietRecord'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    tags=["DietRecord"],
    operation_summary="添加飲食紀錄",
    operation_description="",
    request_body=addDietRecordRequestBody,
    responses=addDietRecordResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addDietRecord(request):
    try:
        user = Users.objects.get(id=request.data['user_id'])
        foodType = FoodType.objects.get(id=request.data['food_type_id'])
        store = Store.objects.get(id=request.data['store_id'])
    except Users.DoesNotExist:
        return Response(FormatErrorResponse('DietRecord'), status=400)
    
    newDietRecord = request.data
    newDietRecord['food_type_id'] = foodType
    newDietRecord['store_id'] = store
    newDietRecord['user_id'] = user

    serializer = DietRecordSerializer(data=newDietRecord)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('DietRecord'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["DietRecord"],
    operation_summary="更新食物",
    operation_description="",
    request_body=addFoodRequestBody,
    responses=updateFoodResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateDietRecord(request, id):
    try:
        updateDietRecord = DietRecord.objects.get(id=id)
    except DietRecord.DoesNotExist:
        return Response(NotFoundResponse('DietRecord'), status=404)

    if (request.data['food_type_id'] == '自訂'):
        updateDietRecord.date = request.data['date']
        updateDietRecord.serving_amount = request.data['serving_amount']
        updateDietRecord.label = request.data['label']
        updateDietRecord.name = request.data['name']
        updateDietRecord.calorie = request.data['calorie']
        updateDietRecord.size = request.data['size']
        updateDietRecord.unit = request.data['unit']
        updateDietRecord.protein = request.data['protein']
        updateDietRecord.fat = request.data['fat']
        updateDietRecord.carb = request.data['carb']
        updateDietRecord.sodium = request.data['sodium']
    else:
        updateDietRecord.date = request.data['date']
        updateDietRecord.serving_amount = request.data['serving_amount']
        updateDietRecord.label = request.data['label']

    
    updateDietRecord.save()

    serializer = DietRecordSerializer(updateDietRecord)
    return Response(serializer.data, status=200)