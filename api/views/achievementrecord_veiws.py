from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import AchievementRecord, UserAchievement
from ..serializers import AchievementRecordSerializer
from ..utils.response import *

def addAchievementRecord(user_id):
    newAchievementRecord = { "user_id": user_id, }
    serializer = AchievementRecordSerializer(data=newAchievementRecord)
    if (serializer.is_valid()):
        serializer.save()
        return "SuccessFully"
    else:
        return "Failed"

def updateContinuousBonus(user_id, operatorCode):
    achievementRecord = AchievementRecord.objects.get(user_id=user_id)

    # 1: 有連續
    # 2: 無連續
    if (operatorCode == 1):
        achievementRecord.continuous_bonus += 1
    else:
        achievementRecord.continuous_bonus = 1

    achievementRecord.save()

    print("continuous_bonus", achievementRecord.continuous_bonus)

    if (achievementRecord.continuous_bonus == 30):
        achievementRecord.continuous_bonus_state = False
        achievementRecord.save()

        userAchievement = UserAchievement.objects.get(user_id=user_id, achievement_id=2)
        userAchievement.is_achieve = True
        userAchievement.save()

    return achievementRecord.continuous_bonus
