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

def updateUserAchievement(user_id, achievement_id, is_achieve):
    userAchievement = UserAchievement.objects.get(user_id=user_id, achievement_id=achievement_id)
    userAchievement.is_achieve = is_achieve
    userAchievement.save()

def addAndcheckBodyBooster(user_id, addAmount):
    achievementRecord = AchievementRecord.objects.get(user_id=user_id)
    achievementRecord.count_achieve += addAmount
    achievementRecord.save()

    result = {
        "isBodyBooster": "no",
        "count_achieve": 0
    }

    if (achievementRecord.count_achieve == 13):
        achievementRecord.count_achieve += 1
        achievementRecord.count_achieve_state = False
        updateUserAchievement(user_id, 1, True)
        achievementRecord.save()
        result["isBodyBooster"] = "yes"
    
    result["count_achieve"] = achievementRecord.count_achieve
    return result

def updateContinuousBonus(user_id, operatorCode):
    achievementRecord = AchievementRecord.objects.get(user_id=user_id)
    isBodyBooster = "no"

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
        achievementRecord.count_achieve += 1
        achievementRecord.save()

        # check bodybooster
        if (achievementRecord.count_achieve == 13):
            isBodyBooster = "yes"
            achievementRecord.count_achieve_state = False
            updateUserAchievement(user_id, 1, True)
            achievementRecord.count_achieve += 1
            achievementRecord.save()

        updateUserAchievement(user_id, 2, True)

    result = {
        "isBodyBooster": isBodyBooster,
        "continuoust_bonus": achievementRecord.continuous_bonus
    }
    return result

