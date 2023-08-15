from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from datetime import datetime, timedelta

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import DailyBonus, Users, AchievementRecord
from ..serializers import DailyBonusSerializer
from ..utils.response import *
from ..swagger.dailybonus import *
from ..views.achievementrecord_veiws import updateContinuousBonus

@swagger_auto_schema(
    methods=['GET'],
    tags=["DailyBonus"],
    operation_summary='查詢指定使用者簽到記錄',
    operation_description="輸入user id，查詢使用者簽到記錄",
    responses=getDailyBonusByIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getDailyBonusByUserId(request, id):
    all_dailyBonus = DailyBonus.objects.filter(user_id=id)

    if (len(all_dailyBonus) == 0):
        return Response(NotFoundResponse('DailyBonus'), status=404)
    else:
        serializer = DailyBonusSerializer(all_dailyBonus, many=True)
        return Response(serializer.data, status=200)
    

@swagger_auto_schema(
    methods=['POST'],
    tags=["DailyBonus"],
    operation_summary="添加簽到記錄",
    operation_description="輸入 user id 添加簽到記錄",
    responses=addDailyBonusByIdResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addDailyBonusByUserId(request, id):
    try:
        user = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    all_dailyBonus = DailyBonus.objects.filter(user_id=id).order_by('-date')
    now = timezone.now()

    continuousBonus = 0

    if (all_dailyBonus.count() != 0):
        if now.date() == all_dailyBonus[0].date.date():
            return Response({ "message": 'This account was signed in today.'}, status=400)
        
        achievementRecord = AchievementRecord.objects.get(user_id=id)
        if (achievementRecord.continuous_bonus_state == True):
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            if (all_dailyBonus[0].date.date() == yesterday.date()):
                continuousBonus = updateContinuousBonus(id, 1)
            else:
                continuousBonus = updateContinuousBonus(id, 2)
        else:
            continuousBonus = 30
    else:
        achievementRecord = AchievementRecord.objects.get(user_id=id)
        if (achievementRecord.continuous_bonus_state == True):
            continuousBonus = updateContinuousBonus(id, 2)
        else:
            continuousBonus = 30

    newDailyBonus = {
        "user_id": id
    }

    serializer = DailyBonusSerializer(data=newDailyBonus)

    if (serializer.is_valid()):
        serializer.save()

        result = serializer.data

        if (continuousBonus == 30):
            result["achievement"] = "Achievement of id: 2 has been achieved."
            result["continuous_bonus"] = continuousBonus
        else:
            result["achievement"] = "Achievement of id: 2 has not yet been achieved."
            result["continuous_bonus"] = continuousBonus

        return Response(result, status=200)
    else:
        print(serializer.errors)
        return Response(FormatErrorResponse('DailyBonus'), status=400)