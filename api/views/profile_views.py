from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Profile, Users
from ..serializers import ProfileSerializer
from ..utils.response import *
from .user_views import updateUserStatus

@swagger_auto_schema(
    methods=['GET'],
    tags=["Profile"],
    operation_summary='查詢全部的使用者個人資料',
    operation_description="",
    responses={
            200: 'ProfileObject',
            404: str(NotFoundResponse('Profile'))
    }
)
@api_view(['GET'])
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
    responses={
            200: 'ProfileObject',
            404: str(NotFoundResponse('Profile'))
    }
)
@api_view(['GET'])
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
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='名字(暱稱)'
            ),
            'gender': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='性別 1:男生, 2:女生'
            ),
            'birthday': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='出生年月日, 格式: yyyy-mm-dd, 範例: 2023-05-23'
            ),
            'height': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='身高, 單位公分, 浮點數'
            ),
            'weight': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='體重, 單位公斤, 浮點數'
            ),
            'userID': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='相對應的user id, foreignkey'
            )
        }
    ),
    responses={
            200: 'ProfileObject',
            400: str(FormatErrorResponse('Profile')),
            404: str(NotFoundResponse('userID'))
    }
)
@api_view(['POST'])
def addProfile(request):

    try:
        rUser = Users.objects.get(id=request.data['userID'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('userID'), status=404)
    
    newProfile = {
        "name": request.data['name'],
        "gender": request.data['gender'],
        "birthday": datetime.strptime(request.data['birthday'], "%Y-%m-%d").date(),
        "height": request.data['height'],
        "weight": request.data['weight'],
        "user_id": request.data['userID']
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
    operation_description="可更新欄位只有以下輸入之欄位，可傳入完整的profile",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='名字(暱稱)'
            ),
            'gender': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='性別 1:男生, 2:女生'
            ),
            'birthday': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='出生年月日, 格式: yyyy-mm-dd, 範例: 2023-05-23'
            ),
            'height': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='身高, 單位公分, 浮點數'
            ),
            'weight': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='體重, 單位公斤, 浮點數'
            ),
        }
    ),
    responses={
            200: 'ProfileObject',
            400: str(FormatErrorResponse('Profile')),
            404: str(NotFoundResponse('Profile'))
    }
)
@api_view(['PUT'])
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
    responses={
            200: '{ "message": "Profile deleted successfully." }',
            404: str(NotFoundResponse('Profile'))
    }
)
@api_view(['DELETE'])
def deleteProfile(request, id):
    try:
        delProfile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(NotFoundResponse('Profile'), status=404)
    
    delProfile.delete()
    return Response({ "message": "Profile deleted successfully." }, status=200)