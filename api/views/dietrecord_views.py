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
    operation_summary='查詢指定使用者飲食紀錄',
    operation_description="輸入id，查詢使用者飲食紀錄",
    responses=getDietRecordByIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getDietRecordById(request, id):
    try:
        all_dietRecord = DietRecord.objects.filter(user_id=id)

        if (len(all_dietRecord) == 0):
            return Response(NotFoundResponse('DietRecord'), status=404)
        serializer = DietRecordSerializer(all_dietRecord, many=True)
        return Response(serializer.data, status=200)
    except DietRecord.DoesNotExist:
        return Response(NotFoundResponse('DietRecord'), status=404)
    
@swagger_auto_schema(
    methods=['POST'],
    tags=["DietRecord"],
    operation_summary="添加單筆飲食紀錄",
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

    serializer = DietRecordSerializer(data=newDietRecord)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('DietRecord'), status=400)

@swagger_auto_schema(
    methods=['POST'],
    tags=["DietRecord"],
    operation_summary="添加多筆飲食紀錄",
    operation_description="",
    request_body=addDietRecordListRequestBody,
    responses=addDietRecordResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addDietRecordList(request):
    try:
        user = Users.objects.get(id=request.data['user_id'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=400)
    
    newDietRecordList = []
    for item in request.data['items']:
        newDietRecordList.append({
            "date": request.data['date'],
            "label": request.data['label'],
            "user_id": request.data['user_id'],
            "name": item['name'],
            "calorie": item['calorie'],
            "size": item['size'],
            "unit": item['unit'],
            "protein": item['protein'],
            "fat": item['fat'],
            "carb": item['carb'],
            "sodium": item['sodium'],
            "modify": item['modify'],
            "food_type_id": item['food_type_id'],
            "store_id": item['store_id'],
        })
    
    serializer = DietRecordSerializer(data=newDietRecordList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('DietRecord'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["DietRecord"],
    operation_summary="更新飲食紀錄",
    operation_description="",
    request_body=addDietRecordRequestBody,
    responses=updateDietRecordResponses
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

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["DietRecord"],
    operation_summary='刪除指定id的飲食紀錄',
    operation_description="輸入id，刪除飲食紀錄",
    responses=deleteDietRecordResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteDietRecord(request, id):
    try:
        delFood = DietRecord.objects.get(id=id)
    except DietRecord.DoesNotExist:
        return Response(NotFoundResponse('DietRecord'), status=404)

    delFood.delete()
    return Response({"message": "DietRecord deleted successfully."}, status=200)
