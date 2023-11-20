from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import NotificationHistory, Users
from ..serializers import NotificationHistorySerializer
from ..utils.response import *
from ..swagger.notificationhistory import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["NotificationHistory"],
    operation_summary='查詢指定使用者的通知記錄',
    operation_description="輸入user id，查詢使用者通知記錄",
    responses=getNotificationHistoryByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getNotificationHistoryByUserId(request, id):
    notificationHistoryList = NotificationHistory.objects.filter(user_id=id)

    if (len(notificationHistoryList) == 0):
        return Response(NotFoundResponse('NotificationHistory'), status=404)
    else:
        serializer = NotificationHistorySerializer(notificationHistoryList, many=True)
        return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['POST'],
    tags=["NotificationHistory"],
    operation_summary="添加通知記錄",
    operation_description="",
    request_body=addNotificationHistoryRequestBody,
    responses=addNotificationHistoryResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addNotificationHistory(request):
    try:
        user = Users.objects.get(id=request.data['user_id'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'))
    
    newNotificationHistory = request.data
    serializer = NotificationHistorySerializer(data=newNotificationHistory)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(FormatErrorResponse('NotificationHistory'), status=400)
    

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["NotificationHistory"],
    operation_summary='刪除通知記錄',
    operation_description="輸入id，刪除通知記錄",
    responses=deleteNotificationHistoryResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteNotificationHistory(request, id):
    try:
        delNotificationHistory = NotificationHistory.objects.get(id=id)
    except NotificationHistory.DoesNotExist:
        return Response(NotFoundResponse('NotificationHistory'), status=404)
    
    deleteNotificationHistory.delete()
    return Response({ "message": "NotificationHistory deleted successfully." }, status=200)
