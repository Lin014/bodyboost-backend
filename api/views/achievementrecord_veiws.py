from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import AchievementRecord, UserAchievement, UserAchievedSport, Sport
from ..serializers import AchievementRecordSerializer, UserAchievedSportSerializer
from ..utils.response import *

def addAchievementRecord(user_id, sport_record_week_id):
    newAchievementRecord = { "user_id": user_id, "sport_record_week_id": sport_record_week_id }
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

def addUserAchievedSport(user_id, sportList):
    newUserAchievedSport = []
    for sport in sportList:
        try:
            userAchievedSport = UserAchievedSport.objects.get(user_id=user_id, sport_id=sport.id)
        except UserAchievedSport.DoesNotExist:
            newUserAchievedSport.append({
                "sport_id": sport.id,
                "user_id": user_id
            })
    
    if newUserAchievedSport:
        serializer = UserAchievedSportSerializer(data=newUserAchievedSport, many=True)
        if (serializer.is_valid()):
            serializer.save()
            return "Successfully"
        else:
            return "Failed"
    else:
        return "Successfully"

def checkUnlockSportAchievedment(user_id):
    achievementRecord = AchievementRecord.objects.get(user_id=user_id)

    if achievementRecord.count_achieve_state:
        countUserAchievedSport = UserAchievedSport.objects.filter(user_id=user_id).count()
        countSport = Sport.objects.count()

        achievedAchievement = []
        if (achievementRecord.sport_ten_state and countUserAchievedSport == 10):
            achievedAchievement.append(3)
            updateUserAchievement(user_id, 3, True)
            achievementRecord.sport_ten_state = False
            
        if (achievementRecord.sport_twenty_state and countUserAchievedSport == 20):
            achievedAchievement.append(4)
            updateUserAchievement(user_id, 4, True)
            achievementRecord.sport_twenty_state = False
            
        if (achievementRecord.sport_all_state and countUserAchievedSport == countSport):
            achievedAchievement.append(5)
            updateUserAchievement(user_id, 5, True)
            achievementRecord.sport_all_state = False
        
        achievementRecord.save()
        
        checkBodyBooster = addAndcheckBodyBooster(user_id, len(achievedAchievement))
        if (checkBodyBooster['isBodyBooster'] == "yes"):
                achievedAchievement.append(1)
        
        result = {
            "achieved_achievement": achievedAchievement,
            "count_achieve": checkBodyBooster['count_achieve']
        }
    else:
        result = {
            "achieved_achievement": [],
            "count_achieve": 14
        }
    
    return result

