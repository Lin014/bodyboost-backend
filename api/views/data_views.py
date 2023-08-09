from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import StoreSerializer, FoodTypeSerializer, FoodSerializer, SportSerializer, AnimationSerializer, AchievementSerializer
from ..utils.response import *
from ..swagger.data import *
# data
from ..data.store import *
from ..data.food_type import *
from ..data.food import *
from ..data.sport import *
from ..data.animation import *
from ..data.achievement import *

@swagger_auto_schema(
    methods=['POST'],
    tags=["Data"],
    operation_summary="匯入商店資料",
    operation_description="",
    responses=insertDataResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def insertStoreData(request):

    serializer = StoreSerializer(data=storeList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response({"message": "Add successfully."}, status=200)
    else:
        return Response({"message": "Add failed."}, status=400)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Data"],
    operation_summary="匯入食物類型資料",
    operation_description="",
    responses=insertDataResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def insertFoodTypeData(request):

    serializer = FoodTypeSerializer(data=foodTypeList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response({"message": "Add successfully."}, status=200)
    else:
        return Response({"message": "Add failed."}, status=400)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Data"],
    operation_summary="匯入食物資料",
    operation_description="",
    responses=insertDataResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def insertFoodData(request):

    serializer = FoodSerializer(data=foodList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response({"message": "Add successfully."}, status=200)
    else:
        return Response({"message": "Add failed."}, status=400)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Data"],
    operation_summary="匯入運動資料",
    operation_description="",
    responses=insertDataResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def insertSportData(request):

    serializer = SportSerializer(data=sportList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response({"message": "Add successfully."}, status=200)
    else:
        return Response({"message": "Add failed."}, status=400)


@swagger_auto_schema(
    methods=['POST'],
    tags=["Data"],
    operation_summary="匯入動畫資料",
    operation_description="",
    responses=insertDataResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def insertAnimationData(request):

    serializer = AnimationSerializer(data=animationList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response({"message": "Add successfully."}, status=200)
    else:
        return Response({"message": "Add failed."}, status=400)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Data"],
    operation_summary="匯入成就資料",
    operation_description="",
    responses=insertDataResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def insertAchievementData(request):

    serializer = AchievementSerializer(data=achievementList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return Response({"message": "Add successfully."}, status=200)
    else:
        return Response({"message": "Add failed."}, status=400)
