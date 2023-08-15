from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import UserAchievement, Achievement
from ..serializers import UserAchievementSerializer, AchievementSerializer
from ..utils.response import *
from ..swagger.userachievement import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["UserAchievement"],
    operation_summary='查詢使用者成就資料',
    operation_description="輸入使用者id查詢",
    responses=getUserAchievementByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getUserAchievementByUserId(request, id):
    userAchievementList = UserAchievement.objects.filter(user_id=id)

    serializer = UserAchievementSerializer(userAchievementList, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse("UserAchievement"), status=404)
    
    result = serializer.data
    for userAchievement in result:
        achievement = Achievement.objects.get(id=userAchievement['achievement_id'])
        achievementSerializer = AchievementSerializer(achievement)
        del userAchievement["achievement_id"]
        userAchievement["achievement"] = achievementSerializer.data

    return Response(result, status=200)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["UserAchievement"],
    operation_summary='更改使用者成就資料',
    operation_description="輸入userAchievement id更改",
    request_body=updateUserAchievementRequestBody,
    responses=getUserAchievementByUserIdResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateUserAchievement(request, id):
    try:
        userAchievement = UserAchievement.objects.get(id=id)
    except UserAchievement.DoesNotExist:
        return Response(NotFoundResponse('UserAchievement'), status=404)
    
    userAchievement.is_achieve = request.data['is_achieve']
    userAchievement.save()

    serializer = UserAchievementSerializer(userAchievement)
    return Response(serializer.data, status=200)


def addUserAchievementList(userId):
    achievementList = Achievement.objects.all()

    userAchievementList = []
    for achievement in achievementList:
        userAchievementList.append({
            "user_id": userId,
            "achievement_id": achievement.id
        })
    
    serializer = UserAchievementSerializer(data=userAchievementList, many=True)
    if (serializer.is_valid()):
        serializer.save()
        return "Successfully"
    else:
        return "Failed"