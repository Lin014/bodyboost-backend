from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import CustomFood, FoodType, Store, Users
from ..serializers import CustomFoodSerializer
from ..utils.response import *
from ..swagger.customfood import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["CustomFood"],
    operation_summary='查詢全部自訂食物',
    operation_description="",
    responses=getAllCustomFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllCustomFood(request):
    all_food = CustomFood.objects.all()
    serializer = CustomFoodSerializer(all_food, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('CustomFood'), status=404)
    else:
        return Response(serializer.data)


@swagger_auto_schema(
    methods=['POST'],
    tags=["CustomFood"],
    operation_summary="添加自訂食物",
    operation_description="",
    request_body=addCustomFoodRequestBody,
    responses=addCustomFoodResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addCustomFood(request):
    try:
        foodType = FoodType.objects.get(id=request.data['food_type_id'])
        store = Store.objects.get(id=request.data['store_id'])
        user = Users.objects.get(id=request.data['user_id'])
    except FoodType.DoesNotExist or Store.DoesNotExist or Users.DoesNotExist:
        return Response(FormatErrorResponse('Food'), status=400)
    
    newFood = request.data

    serializer = CustomFoodSerializer(data=newFood)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('CustomFood'), status=400)


@swagger_auto_schema(
    methods=['PUT'],
    tags=["CustomFood"],
    operation_summary="更新自訂食物",
    operation_description="",
    request_body=addCustomFoodRequestBody,
    responses=updateCustomFoodResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateCustomFood(request, id):
    try:
        updateFood = CustomFood.objects.get(id=id)
    except CustomFood.DoesNotExist:
        return Response(NotFoundResponse('CustomFood'), status=404)
    
    try:
        foodType = FoodType.objects.get(id=request.data['food_type_id'])
        store = Store.objects.get(id=request.data['store_id'])
    except FoodType.DoesNotExist or Store.DoesNotExist:
        return Response(FormatErrorResponse('CustomFood'), status=400)

    updateFood.name = request.data['name']
    updateFood.calorie = request.data['calorie']
    updateFood.size = request.data['size']
    updateFood.unit = request.data['unit']
    updateFood.protein = request.data['protein']
    updateFood.fat = request.data['fat']
    updateFood.carb = request.data['carb']
    updateFood.sodium = request.data['sodium']
    updateFood.food_type = request.data['food_type_id']
    updateFood.store = request.data['store_id']
    updateFood.save()

    serializer = CustomFoodSerializer(updateFood)
    return Response(serializer.data, status=200)


@swagger_auto_schema(
    methods=['DELETE'],
    tags=["CustomFood"],
    operation_summary='刪除指定id的食物',
    operation_description="輸入id，刪除食物",
    responses=deleteCustomFoodResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteCustomFood(request, id):
    try:
        delFood = CustomFood.objects.get(id=id)
    except CustomFood.DoesNotExist:
        return Response(NotFoundResponse('CustomFood'), status=404)

    delFood.delete()
    return Response({"message": "Custom Food deleted successfully."}, status=200)
