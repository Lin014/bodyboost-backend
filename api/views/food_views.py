from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from itertools import chain

from ..models import Food, FoodType, Store
from ..serializers import FoodSerializer
from ..utils.response import *
from ..swagger.food import *
from .pagination_views import paginator
from ..swagger.page import pageManualParameters

@swagger_auto_schema(
    methods=['GET'],
    tags=["Food"],
    operation_summary='查詢全部食物',
    operation_description="",
    manual_parameters=pageManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllFood(request):
    all_food = Food.objects.all()
    result_page = paginator.paginate_queryset(all_food, request)
    serializer = FoodSerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Food'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Food"],
    operation_summary="添加食物",
    operation_description="",
    request_body=addFoodRequestBody,
    responses=addFoodResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addFood(request):
    try:
        foodType = FoodType.objects.get(id=request.data['food_type_id'])
        store = Store.objects.get(id=request.data['store_id'])
    except FoodType.DoesNotExist or Store.DoesNotExist:
        return Response(FormatErrorResponse('Food'), status=400)
    
    newFood = request.data

    serializer = FoodSerializer(data=newFood)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('Food'), status=400)


@swagger_auto_schema(
    methods=['PUT'],
    tags=["Food"],
    operation_summary="更新食物",
    operation_description="",
    request_body=addFoodRequestBody,
    responses=updateFoodResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateFood(request, id):
    try:
        updateFood = Food.objects.get(id=id)
    except Food.DoesNotExist:
        return Response(NotFoundResponse('Food'), status=404)
    
    try:
        foodType = FoodType.objects.get(id=request.data['food_type_id'])
        store = Store.objects.get(id=request.data['store_id'])
    except FoodType.DoesNotExist or Store.DoesNotExist:
        return Response(FormatErrorResponse('Food'), status=400)

    updateFood.name = request.data['name']
    updateFood.calorie = request.data['calorie']
    updateFood.size = request.data['size']
    updateFood.unit = request.data['unit']
    updateFood.protein = request.data['protein']
    updateFood.fat = request.data['fat']
    updateFood.carb = request.data['carb']
    updateFood.sodium = request.data['sodium']
    updateFood.modify = request.data['modify']
    updateFood.food_type_id = foodType
    updateFood.store_id = store
    updateFood.save()

    serializer = FoodSerializer(updateFood)
    return Response(serializer.data, status=200)


@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Food"],
    operation_summary='刪除指定id的食物',
    operation_description="輸入id，刪除食物",
    responses=deleteFoodResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteFood(request, id):
    try:
        delFood = Food.objects.get(id=id)
    except Food.DoesNotExist:
        return Response(NotFoundResponse('Food'), status=404)

    delFood.delete()
    return Response({"message": "Food deleted successfully."}, status=200)
