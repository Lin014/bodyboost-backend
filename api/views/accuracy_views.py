from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import Accuracy, SportRecordItem
from ..serializers import AccuracySerializer
from ..utils.response import *
from ..swagger.accuracy import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Accuracy"],
    operation_summary='查詢某個sportRecordItem的準確率資料',
    operation_description="",
    responses=getAccuracyBySportRecordItemIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAccuracyBySportRecordItemId(request, id):
    accuracy = Accuracy.objects.filter(sport_record_item_id=id)

    if (len(accuracy) == 0):
        return Response(NotFoundResponse('Accuracy'), status=404)
    else:
        serializer = AccuracySerializer(accuracy)
        return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Accuracy"],
    operation_summary="添加準確率資料",
    operation_description="",
    request_body=addAccuracyRequestBody,
    responses=addAccuracyResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addAccuracy(request):
    try:
        sportRecordItem = SportRecordItem.objects.get(id=request.data['sport_record_item_id'])
    except SportRecordItem.DoesNotExist:
        return Response(NotFoundResponse('SportRecordItem'), status=404)
    
    newAccuracy = request.data
    serializer = AccuracySerializer(data=newAccuracy)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(FormatErrorResponse('Accuracy'), status=400)
    
@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Accuracy"],
    operation_summary='刪除準確率資料',
    operation_description="輸入id，刪除準確率資料",
    responses=deleteAccuracyResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteAccuracy(request, id):
    try:
        delAccuracy = Accuracy.objects.get(id=id)
    except Accuracy.DoesNotExist:
        return Response(NotFoundResponse('Accuracy'), status=404)
    
    delAccuracy.delete()
    return Response({ "message": "Accuracy deleted successfully." }, status=200)
