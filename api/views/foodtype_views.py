from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import FoodType
from ..serializers import FoodTypeSerializer
from ..utils.response import *
from ..swagger.foodtype import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["FoodType"],
    operation_summary='查詢全部食物類別',
    operation_description="",
    responses=getAllFoodTypeResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllFoodType(request):
    all_food_type = FoodType.objects.all()
    serializer = FoodTypeSerializer(all_food_type, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('FoodType'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    tags=["FoodType"],
    operation_summary="添加食物類別",
    operation_description="",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=addFoodTypeRequestBody
    ),
    responses=addFoodTypeResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addFoodType(request):

    try:
        oFoodType = FoodType.objects.get(name=request.data['type'])
        return Response({ "message": "FoodType already exists.", "foodType": oFoodType }, status=400)
    except FoodType.DoesNotExist:
        newFoodType = FoodType.objects.create(name=request.data['type'])
        serializer = FoodTypeSerializer(newFoodType)
        return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["FoodType"],
    operation_summary="更新食物類別",
    operation_description="",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=updateFoodTypeRequestBody
    ),
    responses=updateFoodTypeResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateFoodType(request, id):
    try:
        updateFoodType = FoodType.objects.get(id=id)
    except FoodType.DoesNotExist:
        return Response(NotFoundResponse('FoodType'), status=404)
    
    updateFoodType.type = request.data['type']
    updateFoodType.save()

    serializer = FoodTypeSerializer(updateFoodType)
    return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["FoodType"],
    operation_summary='刪除指定id的食物類別',
    operation_description="輸入id，刪除食物類別",
    responses=deleteFoodTypeResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteFoodType(request, id):
    try:
        delFoodType = FoodType.objects.get(id=id)
    except FoodType.DoesNotExist:
        return Response(NotFoundResponse('FoodType'), status=404)
    
    delFoodType.delete()
    return Response({ "message": "FoodType deleted successfully." }, status=200)