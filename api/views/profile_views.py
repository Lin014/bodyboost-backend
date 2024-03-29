from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from drf_yasg import openapi

from ..models import Profile, Users, GoalHistory, AchievementRecord, WeigthtHistory, GoalHistory
from ..serializers import ProfileSerializer
from ..utils.response import *
from .user_views import updateUserStatus
from ..utils.validate import validateImage
from ..utils.osFileManage import deleteFile
from ..swagger.profile import *
from ..views.weighthistory_views import addWeightHistory
from ..views.bodyfathistory_views import addBodyFatHistory
from ..views.goalhistory_views import addGoalHistory
from ..views.userachievement_views import addUserAchievementList
from ..views.achievementrecord_veiws import addAchievementRecord
from ..views.sportrecordweek_views import addSportRecordWeek
from ..views.achievementrecord_veiws import updateUserAchievement, addAndcheckBodyBooster

@swagger_auto_schema(
    methods=['GET'],
    tags=["Profile"],
    operation_summary='查詢全部的使用者個人資料',
    operation_description="",
    responses=getAllProfileResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllProfile(request):
    all_profile = Profile.objects.all()

    serializer = ProfileSerializer(all_profile, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Profile'), status=404)
    else:
        result = serializer.data
        for profile in result:
            goalHistory = GoalHistory.objects.get(id=profile['goal_id'])
            del profile['goal_id']
            profile['goal'] = goalHistory.goal
            
        return Response(result)
        

@swagger_auto_schema(
    methods=['GET'],
    tags=["Profile"],
    operation_summary='查詢指定使用者id的個人資料',
    operation_description="輸入使用者id，查詢使用者個人資料",
    responses=getProfileByIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getProfileById(request, id):
    try:
        p = Profile.objects.get(user=id)
        serializer = ProfileSerializer(p)

        result = serializer.data
        goalHistory = GoalHistory.objects.get(id=result['goal_id'])
        del result['goal_id']
        result['goal'] = goalHistory.goal
 
        return Response(result, status=200)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
@swagger_auto_schema(
    methods=['POST'],
    tags=["Profile"],
    operation_summary="添加使用者個人資料",
    operation_description="必須和user表作關聯",
    request_body=addProfileRequestBody,
    responses=addProfileResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addProfile(request):

    try:
        rUser = Users.objects.get(id=request.data['userID'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('userID'), status=404)

    newProfile = request.data.copy()
    newProfile["user"] = request.data['userID']
    del newProfile["userID"]

    # add goal history
    newGoalHistory = addGoalHistory(request.data['userID'], "health")
    print(newGoalHistory['id'])

    newProfile['goal_id'] = newGoalHistory['id']
    
    serializer = ProfileSerializer(data=newProfile)
    
    if (serializer.is_valid()):
        serializer.save()
        updateUserStatus(request.data['userID'], 'success')
        # add weight history
        addWeightHistory(request.data['userID'], request.data['weight'])
        # add userachievement
        addUserAchievementList(request.data['userID'])
        # add sport achievement data
        newSportRecordWeek = addSportRecordWeek(rUser.id, timezone.now())
        addAchievementRecord(request.data['userID'], newSportRecordWeek['id'])

        result = serializer.data
        del result['goal_id']
        result['goal'] = newGoalHistory['goal']

        return Response(result)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)
    
@swagger_auto_schema(
    methods=['PUT'],
    tags=["Profile"],
    operation_summary="更新使用者個人資料",
    operation_description="輸入user id, 可更新欄位只有以下輸入之欄位，需完整傳入以下欄位之json，就算不需要修改的欄位也要",
    request_body=updateProfileRequestBody,
    responses=updateProfileResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateProfileByUserId(request, id):
    try:
        updateProfile = Profile.objects.get(user=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    updateProfile.name = request.data['name']
    updateProfile.gender = request.data['gender']
    updateProfile.birthday = datetime.strptime(request.data['birthday'], "%Y-%m-%d").date()
    updateProfile.height = request.data['height']

    serializer = ProfileSerializer(updateProfile)
    if (serializer.is_valid):
        updateProfile.save()

        result = serializer.data
        goalHistory = GoalHistory.objects.get(id=result['goal_id'])
        del result['goal_id']
        result['goal'] = goalHistory.goal

        return Response(result, status=200)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Profile"],
    operation_summary="更新使用者個人資料",
    operation_description="輸入user id, 可更新欄位只有以下輸入之欄位，需完整傳入以下欄位之json，就算不需要修改的欄位也要",
    request_body=updateWeightByUserIdRequestBody,
    responses=updateProfileResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateWeightByUserId(request, id):
    try:
        updateProfile = Profile.objects.get(user=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    updateProfile.weight = request.data['weight']
    updateProfile.weight_goal = request.data['weight_goal']

    serializer = ProfileSerializer(updateProfile)
    if (serializer.is_valid):
        updateProfile.save()

        # add weight history
        addWeightHistory(serializer.data['user'], request.data['weight'])

        result = serializer.data
        goalHistory = GoalHistory.objects.get(id=result['goal_id'])
        del result['goal_id']
        result['goal'] = goalHistory.goal

        return Response(result, status=200)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)


@swagger_auto_schema(
    methods=['GET'],
    tags=["Profile"],
    operation_summary='判斷 是否達到體重成就',
    operation_description="輸入 user id",
)
@api_view(['GET'])
def checkWeight(request, id):
    profile = Profile.objects.get(user=id)
    achievementRecord = AchievementRecord.objects.get(user_id=id)
    goalHistory = profile.goal_id
    achievedAchievement =[]

    if achievementRecord.lose_two_weight_state or achievementRecord.lose_ten_weight_state:
        current_date = timezone.now()
        time_difference = current_date - goalHistory.start_date
        days_difference = time_difference.days

        if (days_difference >= 30):
            earily_weight_history = WeigthtHistory.objects.filter(date__gte=goalHistory.start_date).order_by('-date').first()

            if earily_weight_history:
                earilyWeight = earily_weight_history.weight
                latestWeight = profile.weight
                if ((latestWeight - earilyWeight) >= 2):
                    if (profile.weight_goal is not None and (latestWeight <= profile.weight_goal)):
                        achievedAchievement.append(8)
                        updateUserAchievement(id, 8, True)
                        achievementRecord.lose_two_weight_state = False
        elif(days_difference >= 90):
            earily_weight_history = WeigthtHistory.objects.filter(date__gte=goalHistory.start_date).order_by('-date').first()

            if earily_weight_history:
                earilyWeight = earily_weight_history.weight
                latestWeight = profile.weight
                if ((latestWeight - earilyWeight) >= 10):
                    achievedAchievement.append(9)
                    updateUserAchievement(id, 9, True)
                    achievementRecord.lose_two_weight_state = False


    achievementRecord.save()

    if achievementRecord.count_achieve_state:
        checkBodyBooster = addAndcheckBodyBooster(id, len(achievedAchievement))
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

    return Response(result, status=200)


@swagger_auto_schema(
    methods=['PUT'],
    tags=["Profile"],
    operation_summary="更新使用者個人資料",
    operation_description="輸入user id, 可更新欄位只有以下輸入之欄位，需完整傳入以下欄位之json，就算不需要修改的欄位也要",
    request_body=updateBodyFatByUserIdRequestBody,
    responses=updateProfileResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateBodyFatByUserId(request, id):
    try:
        updateProfile = Profile.objects.get(user=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    updateProfile.body_fat = request.data['body_fat']

    serializer = ProfileSerializer(updateProfile)
    if (serializer.is_valid):
        updateProfile.save()

        # add body fat history
        addBodyFatHistory(serializer.data['user'], request.data['body_fat'])

        result = serializer.data
        goalHistory = GoalHistory.objects.get(id=result['goal_id'])
        del result['goal_id']
        result['goal'] = goalHistory.goal

        return Response(result, status=200)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)
    
@swagger_auto_schema(
    methods=['PUT'],
    tags=["Profile"],
    operation_summary="更新使用者個人資料",
    operation_description="輸入user id, 可更新欄位只有以下輸入之欄位，需完整傳入以下欄位之json，就算不需要修改的欄位也要",
    request_body=updateGoalByUserIdRequestBody,
    responses=updateProfileResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateGoalByUserId(request, id):
    try:
        updateProfile = Profile.objects.get(user=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    newGoalHistory = addGoalHistory(id, request.data['goal'])

    goalHistory = GoalHistory.objects.get(id=newGoalHistory['id'])
    
    updateProfile.goal_id = goalHistory

    serializer = ProfileSerializer(updateProfile)
    if (serializer.is_valid):
        updateProfile.save()

        result = serializer.data
        del result['goal_id']
        result['goal'] = newGoalHistory['goal']

        return Response(result, status=200)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Profile"],
    operation_summary='刪除指定id的使用者個人資料',
    operation_description="輸入profile id，刪除使用者個人資料",
    responses=deleteProfileResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteProfile(request, id):
    try:
        delProfile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    delProfile.delete()
    return Response({ "message": "Profile deleted successfully." }, status=200)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Profile"],
    operation_summary="上傳使用者大頭照",
    operation_description="輸入使用者id，上傳大頭貼",
    request_body=uploadProfileImageRequestBody,
    responses=uploadProfileImageResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def uploadProfileImage(request, id):
    try:
        profile = Profile.objects.get(user=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    image = request.data['image']
    print(image)

    if (validateImage(image)):
        # delete old file
        deleteFile(profile.image)
        # store new file and update path to database
        profile.image = image
        profile.save()
        # convert profile object to json format
        serializer = ProfileSerializer(profile)

        result = serializer.data
        goalHistory = GoalHistory.objects.get(id=result['goal_id'])
        del result['goal_id']
        result['goal'] = goalHistory.goal

        return Response(result)
    else:
        return Response(FormatErrorResponse('Image'))
