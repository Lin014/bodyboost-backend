from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import BodyFatHistory
from ..serializers import BodyFatHistorySerializer
from ..utils.response import *
from ..swagger.bodyfathistory import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["BodyFatHistory"],
    operation_summary='查詢某個使用者的體脂率歷史記錄',
    operation_description="輸入 user id 查詢",
    responses=getBodyFatHistoryByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def geBodyFatHistoryByUserId(request, id):
    bodyFatHistoryList = BodyFatHistory.objects.filter(user_id=id).order_by('date')

    if (len(bodyFatHistoryList) == 0):
        return Response(NotFoundResponse('BodyFat'), status=404)
    else:
        serializer = BodyFatHistorySerializer(bodyFatHistoryList, many=True)
        return Response(serializer.data, status=200)

def getLatestBodyFatHistory(userId):
    bodyFatHistoryList = BodyFatHistory.objects.filter(user_id=userId).order_by('-date')

    if (len(bodyFatHistoryList) == 0):
        return -1
    else:
        return bodyFatHistoryList[0]


def addBodyFatHistory(userId, bodyFat):
    newBodyFatHistory = {
        'body_fat': bodyFat,
        'user_id': userId,
    }

    serializer = BodyFatHistorySerializer(data=newBodyFatHistory)
    if (serializer.is_valid()):
        serializer.save()
    else:
        return Response(FormatErrorResponse('BodyFatHistory'), status=400)