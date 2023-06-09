from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Profile, Users
from ..serializers import ProfileSerializer
from ..utils.response import *
from .user_views import updateUserStatus
from ..utils.validate import validateImage
from ..utils.osFileManage import deleteFile
from ..swagger.profile import *

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
        return Response(serializer.data)
        

@swagger_auto_schema(
    methods=['GET'],
    tags=["Profile"],
    operation_summary='查詢指定id的使用者個人資料',
    operation_description="輸入id，查詢使用者個人資料",
    responses=getProfileByIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getProfileById(request, id):
    try:
        p = Profile.objects.get(id=id)
        serializer = ProfileSerializer(p)
        return Response(serializer.data, status=200)
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
    
    newProfile = {
        "name": request.data['name'],
        "gender": request.data['gender'],
        "birthday": request.data['birthday'],
        "height": request.data['height'],
        "weight": request.data['weight'],
        "user": request.data['userID']
    }
    
    serializer = ProfileSerializer(data=newProfile)
    
    if (serializer.is_valid()):
        serializer.save()
        updateUserStatus(request.data['userID'], 'success')
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)
    
@swagger_auto_schema(
    methods=['PUT'],
    tags=["Profile"],
    operation_summary="更新使用者個人資料",
    operation_description="可更新欄位只有以下輸入之欄位，需完整傳入以下欄位之json，就算不需要修改的欄位也要",
    request_body=updateProfileRequestBody,
    responses=updateProfileResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateProfile(request, id):
    try:
        updateProfile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    updateProfile.name = request.data['name']
    updateProfile.gender = request.data['gender']
    updateProfile.birthday = datetime.strptime(request.data['birthday'], "%Y-%m-%d").date()
    updateProfile.height = request.data['height']
    updateProfile.weight = request.data['weight']

    print(updateProfile.birthday)

    serializer = ProfileSerializer(updateProfile)
    if (serializer.is_valid):
        updateProfile.save()
        return Response(serializer.data, status=200)
    else:
        return Response(FormatErrorResponse('Profile'), status=400)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Profile"],
    operation_summary='刪除指定id的使用者個人資料',
    operation_description="輸入id，刪除使用者個人資料",
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
    operation_description="",
    request_body=uploadProfileImageRequestBody,
    responses=uploadProfileImageResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def uploadProfileImage(request, id):
    try:
        profile = Profile.objects.get(id=id)
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
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('Image'))
