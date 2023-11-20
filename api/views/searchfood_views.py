from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from itertools import chain

from ..models import Food, CustomFood
from ..serializers import FoodSerializer
from ..utils.response import *
from ..swagger.food import *
from .pagination_views import paginator
from ..swagger.page import pageManualParameters

@swagger_auto_schema(
    methods=['GET'],
    tags=["SearchFood"],
    operation_summary='查詢符合指定食物類別id的食物',
    operation_description="輸入食物類別id、user id查詢",
    manual_parameters=pageManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getFoodByFoodTypeId(request, id, userId):
    if (id == 1):
        foodList = CustomFood.objects.filter(food_type_id=id, user_id=userId)
    else:
        foodList = Food.objects.filter(food_type_id=id)
    
    result_page = paginator.paginate_queryset(foodList, request)
    serializer = FoodSerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Food'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['GET'],
    tags=["SearchFood"],
    operation_summary='查詢符合指定商店id的食物',
    operation_description="輸入商店id、user id查詢",
    manual_parameters=pageManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getFoodByStoreId(request, id, userId):
    if (id == 1):
        foodList = CustomFood.objects.filter(store_id=id, user_id=userId)
    else:
        foodList = Food.objects.filter(store_id=id)

    result_page = paginator.paginate_queryset(foodList, request)
    serializer = FoodSerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Food'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['GET'],
    tags=["SearchFood"],
    operation_summary='查詢符合指定關鍵字的食物',
    operation_description="輸入關鍵字、user id查詢",
    manual_parameters=nameManualParameters,
    responses=getAllFoodResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getFoodByName(request, userId):
    name = request.query_params.get('name', None)
    if name is None:
        return Response({'message': 'Please provide a name parameter'}, status=400)
    
    customFoodContainFoodList = CustomFood.objects.filter(name=name, user_id=userId)
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

    resultData = [*customFoodContainFoodList, *sorted_queryset]
    result_page = paginator.paginate_queryset(resultData, request)

    serializer = FoodSerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Food'), status=404)
    else:
        return Response(serializer.data)