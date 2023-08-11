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
    methods=['GET'],
    tags=["Food"],
    operation_summary='查詢符合指定食物類別id的食物',
    operation_description="輸入食物類別id查詢",
    manual_parameters=pageManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getFoodByFoodTypeId(request, id):
    foodList = Food.objects.filter(food_type_id=id)
    result_page = paginator.paginate_queryset(foodList, request)
    serializer = FoodSerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Food'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['GET'],
    tags=["Food"],
    operation_summary='查詢符合指定商店id的食物',
    operation_description="輸入商店id查詢",
    manual_parameters=pageManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getFoodByStoreId(request, id):
    foodList = Food.objects.filter(store_id=id)
    result_page = paginator.paginate_queryset(foodList, request)
    serializer = FoodSerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Food'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['GET'],
    tags=["Food"],
    operation_summary='查詢符合指定關鍵字的食物',
    operation_description="輸入關鍵字查詢",
    manual_parameters=nameManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getFoodByName(request):
    name = request.query_params.get('name', None)
    if name is None:
        return Response({'message': 'Please provide a name parameter'}, status=400)
    
    exactFoodList = Food.objects.filter(name=name)
    startWithList = Food.objects.filter(name__istartswith=name)
    containFoodList = Food.objects.filter(name__icontains=name)

    # combined and delete duplicate values
    combinedResultSet = set(chain(exactFoodList, startWithList, containFoodList))
    # turn to list
    combinedResultList = list(combinedResultSet)
    # Sort the combined queryset by exactFood -> startWithFood -> containFood
    sorted_queryset = sorted(
        combinedResultList,
        key=lambda food: (
            food.name == name,            # Exact match comes first
            food.name.startswith(name),  # Startswith match comes second
            food.name.lower().find(name.lower())  # Contain match comes third
        ),
        reverse=True
    )
    result_page = paginator.paginate_queryset(sorted_queryset, request)
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
