from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import WeigthtHistory
from ..serializers import WeightHistorySerializer
from ..utils.response import *
from ..swagger.weighthistory import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["WeightHistory"],
    operation_summary='查詢某個使用者的體重歷史記錄',
    operation_description="輸入 user id 查詢",
    responses=getWeightHistoryByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getWeightHistoryByUserId(request, id):
    weightHistoryList = WeigthtHistory.objects.filter(user_id=id).order_by('date')

    if (len(weightHistoryList) == 0):
        return Response(NotFoundResponse('WeightHistory'), status=404)
    else:
        serializer = WeightHistorySerializer(weightHistoryList, many=True)
        return Response(serializer.data, status=200)


def getLatestWeightHistory(userId):
    weighthistory = WeigthtHistory.objects.filter(user_id=userId).order_by('-date')

    if (len(weighthistory) == 0):
        return -1
    else:
        return weighthistory[0]


def addWeightHistory(userId, weight):
    newHistory = {
        'weight': weight,
        'user_id': userId,
    }

    serializer = WeightHistorySerializer(data=newHistory)
    if (serializer.is_valid()):
        serializer.save()
    else:
        return Response(FormatErrorResponse('Weight History'), status=400)