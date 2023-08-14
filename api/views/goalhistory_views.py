from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import GoalHistory
from ..serializers import GoalHistorySerializer
from ..utils.response import *
from ..swagger.goalhistory import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["GoalHistory"],
    operation_summary='查詢使用者目標變動歷史紀錄',
    operation_description="輸入使用者id查詢",
    responses=getGoalHistoryByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getGoalHistoryByUserId(request, id):
    goalHistoryList = GoalHistory.objects.filter(user_id=id)

    serializer = GoalHistorySerializer(goalHistoryList, many=True)
    if (serializer.data == []):
        return Response(NotFoundResponse("GoalHistory"), status=404)
    else:
        return Response(serializer.data, status=200)

def addGoalHistory(userId, goal):
    newGoalHistory = {
        "goal": goal,
        "user_id": userId,
    }

    serializer = GoalHistorySerializer(data=newGoalHistory)
    if (serializer.is_valid()):
        serializer.save()
        return "Successfully"
    else:
        return "Failed"