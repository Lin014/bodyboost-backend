from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from datetime import datetime, timedelta

from ..models import DietRecord, Users, FoodType, Store, Profile, AchievementRecord
from ..serializers import DietRecordSerializer
from ..utils.response import *
from ..swagger.dietrecord import *
from ..views.achievementrecord_veiws import updateUserAchievement, addAndcheckBodyBooster

@swagger_auto_schema(
    methods=['GET'],
    tags=["DietRecord"],
    operation_summary='查詢指定使用者飲食紀錄',
    operation_description="輸入id，查詢使用者飲食紀錄",
    responses=getDietRecordByIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getDietRecordById(request, id):
    try:
        all_dietRecord = DietRecord.objects.filter(user_id=id)

        if (len(all_dietRecord) == 0):
            return Response(NotFoundResponse('DietRecord'), status=404)
        serializer = DietRecordSerializer(all_dietRecord, many=True)
        return Response(serializer.data, status=200)
    except DietRecord.DoesNotExist:
        return Response(NotFoundResponse('DietRecord'), status=404)
    
@swagger_auto_schema(
    methods=['POST'],
    tags=["DietRecord"],
    operation_summary="添加單筆飲食紀錄",
    operation_description="",
    request_body=addDietRecordRequestBody,
    responses=addDietRecordResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addDietRecord(request):
    try:
        user = Users.objects.get(id=request.data['user_id'])
        foodType = FoodType.objects.get(id=request.data['food_type_id'])
        store = Store.objects.get(id=request.data['store_id'])
    except Users.DoesNotExist:
        return Response(FormatErrorResponse('DietRecord'), status=400)
    
    newDietRecord = request.data

    serializer = DietRecordSerializer(data=newDietRecord)
    if (serializer.is_valid()):
        serializer.save()

        result = [
            serializer.data, 
            { 
                "checkResult": checkDietRecord(request.data['user_id'])
            }
        ]
        return Response(result, status=200)
    else:
        return Response(FormatErrorResponse('DietRecord'), status=400)

@swagger_auto_schema(
    methods=['POST'],
    tags=["DietRecord"],
    operation_summary="添加多筆飲食紀錄",
    operation_description="",
    request_body=addDietRecordListRequestBody,
    responses=addDietRecordResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addDietRecordList(request):
    try:
        user = Users.objects.get(id=request.data['user_id'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=400)
    
    newDietRecordList = []
    for item in request.data['items']:
        newDietRecordList.append({
            "date": request.data['date'],
            "label": request.data['label'],
            "user_id": request.data['user_id'],
            "serving_amount": item['serving_amount'],
            "name": item['name'],
            "calorie": item['calorie'],
            "size": item['size'],
            "unit": item['unit'],
            "protein": item['protein'],
            "fat": item['fat'],
            "carb": item['carb'],
            "sodium": item['sodium'],
            "modify": item['modify'],
            "food_type_id": item['food_type_id'],
            "store_id": item['store_id'],
        })
    
    serializer = DietRecordSerializer(data=newDietRecordList, many=True)
    if (serializer.is_valid()):
        serializer.save()

        result = [
            serializer.data, 
            { 
                "checkResult": checkDietRecord(request.data['user_id'])
            }
        ]
        return Response(result, status=200)
    else:
        return Response(FormatErrorResponse('DietRecord'), status=400)

def checkDietRecord(user_id):
    achievementRecord = AchievementRecord.objects.get(user_id=user_id)
    if (achievementRecord.count_achieve_state == True):
        threeDaysAgo = datetime.now().date() - timedelta(days=3)
        dietRecordList = DietRecord.objects.filter(user_id=user_id, date__lte=threeDaysAgo).order_by('-date')
        profile = Profile.objects.get(user=user_id)

        date = dietRecordList[0].date.date()
        countDataAmount = 0
        countProteinDataAmount = 0
        countSodiumDataAmount = 0
        countCalorie = 0
        countProtein = 0
        countBeanProtein = 0
        countFat = 0
        countCarb = 0
        countSodium = 0
        continuousSodiumDays = 0
        continuousPFCDays = 0
        continuousCalorieDays = 0
        continuousProteinDays = 0
        for dietRecord in dietRecordList:
            print("id: ", dietRecord.id, " date: ", date)

            # 調整數值
            if (dietRecord.modify):
                calorie = (dietRecord.calorie / 100 * dietRecord.serving_amount) if dietRecord.calorie is not None else None
                sodium = (dietRecord.sodium / 100 * dietRecord.serving_amount) if dietRecord.sodium is not None else None
                protein = (dietRecord.protein / 100 * dietRecord.serving_amount) if dietRecord.protein is not None else None
                fat = (dietRecord.fat / 100 * dietRecord.serving_amount) if dietRecord.fat is not None else None
                carb = (dietRecord.carb / 100 * dietRecord.serving_amount) if dietRecord.carb is not None else None
            else:
                calorie = (dietRecord.calorie * dietRecord.serving_amount) if dietRecord.calorie is not None else None
                sodium = (dietRecord.sodium * dietRecord.serving_amount) if dietRecord.sodium is not None else None
                protein = (dietRecord.protein * dietRecord.serving_amount) if dietRecord.protein is not None else None
                fat = (dietRecord.fat * dietRecord.serving_amount) if dietRecord.fat is not None else None
                carb = (dietRecord.carb * dietRecord.serving_amount) if dietRecord.carb is not None else None

            if (date == dietRecord.date.date()):
                # count data
                countDataAmount += 1
                if (achievementRecord.continuous_sodium_state and sodium is not None):
                    countSodium += sodium
                    countSodiumDataAmount += 1

                if (achievementRecord.continuous_calorie_state and calorie is not None):
                    countCalorie += calorie

                if (achievementRecord.continuous_pfc_state and protein is not None):
                    countProtein += protein
                    countProteinDataAmount += 1
                    countFat += fat if fat is not None else 0
                    countCarb += carb if carb is not None else 0

                if (achievementRecord.continuous_protein_state and protein is not None):
                    countBeanProtein += protein if dietRecord.food_type_id is 7 else 0

                print(countCalorie, countProtein, countBeanProtein, countFat, countCarb, countSodium)
            else:
                # 結算 後一天是否達到 achievement 標準
                # 低納達人(10)
                if (achievementRecord.continuous_sodium_state == True):
                    if (countSodiumDataAmount/countDataAmount >= 0.85):
                        if (countSodium >= 186 and countSodium <= 2400):
                            continuousSodiumDays += 1
                # 均衡飲食(11)
                if (achievementRecord.continuous_pfc_state == True):
                    if (countProteinDataAmount/countDataAmount >= 0.85):
                        proteinPercent = (countProtein*4)/countCalorie
                        if (proteinPercent >= 0.1 and proteinPercent <= 0.35):
                            fatPercent = (countFat*9)/countCalorie
                            if (fatPercent >= 0.2 and fatPercent <= 0.3):
                                carbPercent = (countCarb*4)/countCalorie
                                if (carbPercent >= 0.5 and carbPercent <= 0.6):
                                    continuousPFCDays += 1
                # 輕盈生活(12)
                if (achievementRecord.continuous_calorie_state == True):
                    if (profile.gender == 1):
                        if (countCalorie >= 1500 and countCalorie <= 1800):
                            continuousCalorieDays += 1
                    else:
                        if (countCalorie >= 1200 and countCalorie <= 1500):
                            continuousCalorieDays += 1
                # 植物蛋白質達人(13)
                if (achievementRecord.continuous_protein_state == True):
                    if (countBeanProtein > (countProtein * 0.8)):
                        continuousProteinDays += 1
                
                # 清空資料
                countDataAmount = 0
                countProteinDataAmount = 0
                countSodiumDataAmount = 0
                countCalorie = 0
                countProtein = 0
                countBeanProtein = 0
                countFat = 0
                countCarb = 0
                countSodium = 0
                # 判斷 date 是否只差一天
                if ((date - dietRecord.date.date()) == timedelta(days=1)):
                    date = dietRecord.date.date()
                    # count data
                    countDataAmount += 1
                    if (achievementRecord.continuous_sodium_state and sodium is not None):
                        countSodium += sodium
                        countSodiumDataAmount += 1

                    if (achievementRecord.continuous_calorie_state and calorie is not None):
                        countCalorie += calorie

                    if (achievementRecord.continuous_pfc_state and protein is not None):
                        countProtein += protein
                        countProteinDataAmount += 1
                        countFat += fat if fat is not None else 0
                        countCarb += carb if carb is not None else 0

                    if (achievementRecord.continuous_protein_state and protein is not None):
                        countBeanProtein += protein if dietRecord.food_type_id is 7 else 0

                    print(countCalorie, countProtein, countBeanProtein, countFat, countCarb, countSodium)
                else:
                    break
                # 是就 date = 新來的, +資料 or 不是就跳出迴圈
        
        # 統計是否達成天數
        achievedAchievement = []
        if (achievementRecord.continuous_sodium_state and continuousSodiumDays == 30):
            achievedAchievement.append(10)
            updateUserAchievement(user_id, 10, True)
            achievementRecord.continuous_sodium_state = False
        
        if (achievementRecord.continuous_pfc_state and continuousPFCDays == 7):
            achievedAchievement.append(11)
            updateUserAchievement(user_id, 11, True)
            achievementRecord.continuous_pfc_state = False

        if (achievementRecord.continuous_calorie_state and continuousCalorieDays == 7):
            achievedAchievement.append(12)
            updateUserAchievement(user_id, 12, True)
            achievementRecord.continuous_calorie_state = False
        
        if (achievementRecord.continuous_protein_state and continuousProteinDays == 30):
            achievedAchievement.append(13)
            updateUserAchievement(user_id, 13, True)
            achievementRecord.continuous_protein_state = False
        
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

@swagger_auto_schema(
    methods=['PUT'],
    tags=["DietRecord"],
    operation_summary="更新飲食紀錄",
    operation_description="",
    request_body=addDietRecordRequestBody,
    responses=updateDietRecordResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateDietRecord(request, id):
    try:
        updateDietRecord = DietRecord.objects.get(id=id)
    except DietRecord.DoesNotExist:
        return Response(NotFoundResponse('DietRecord'), status=404)

    if (request.data['food_type_id'] == '自訂'):
        updateDietRecord.date = request.data['date']
        updateDietRecord.serving_amount = request.data['serving_amount']
        updateDietRecord.label = request.data['label']
        updateDietRecord.name = request.data['name']
        updateDietRecord.calorie = request.data['calorie']
        updateDietRecord.size = request.data['size']
        updateDietRecord.unit = request.data['unit']
        updateDietRecord.protein = request.data['protein']
        updateDietRecord.fat = request.data['fat']
        updateDietRecord.carb = request.data['carb']
        updateDietRecord.sodium = request.data['sodium']
    else:
        updateDietRecord.date = request.data['date']
        updateDietRecord.serving_amount = request.data['serving_amount']
        updateDietRecord.label = request.data['label']

    
    updateDietRecord.save()

    serializer = DietRecordSerializer(updateDietRecord)
    return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["DietRecord"],
    operation_summary='刪除指定id的飲食紀錄',
    operation_description="輸入id，刪除飲食紀錄",
    responses=deleteDietRecordResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteDietRecord(request, id):
    try:
        delFood = DietRecord.objects.get(id=id)
    except DietRecord.DoesNotExist:
        return Response(NotFoundResponse('DietRecord'), status=404)

    delFood.delete()
    return Response({"message": "DietRecord deleted successfully."}, status=200)
