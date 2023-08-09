from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import WaterHistory, Users
from ..serializers import WaterHistorySerializer
from ..utils.response import *
from ..swagger.waterhistory import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["WaterHistory"],
    operation_summary='查詢某個使用者的飲水歷史記錄',
    operation_description="輸入 user id 查詢",
    responses=getWaterHistoryByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def geWaterHistoryByUserId(request, id):
    waterHistoryList = WaterHistory.objects.filter(user_id=id).order_by('date')

    if (len(waterHistoryList) == 0):
        return Response(NotFoundResponse('WaterHistory'), status=404)
    else:
        serializer = WaterHistorySerializer(waterHistoryList, many=True)
        return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['POST'],
    tags=["WaterHistory"],
    operation_summary="添加飲水資料",
    operation_description="",
    request_body=addWaterHistoryRequestBody,
    responses=addWaterHistoryResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addWaterHistory(request):
    try:
        user = Users.objects.get(id=request.data['user_id'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    newWaterHistory = request.data
    serializer = WaterHistorySerializer(data=newWaterHistory)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(FormatErrorResponse('WaterHistory'), status=400)
    
@swagger_auto_schema(
    methods=['DELETE'],
    tags=["WaterHistory"],
    operation_summary='刪除準確率資料',
    operation_description="輸入id，刪除準確率資料",
    responses=deleteWaterHistoryResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteWaterHistory(request, id):
    try:
        delWaterHistory = WaterHistory.objects.get(id=id)
    except WaterHistory.DoesNotExist:
        return Response(NotFoundResponse('WaterHistory'), status=404)
    
    delWaterHistory.delete()
    return Response({ "message": "WaterHistory deleted successfully." }, status=200)
