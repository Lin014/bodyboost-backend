from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import profile, users
from ..serializers import ProfileSerializer, UsersSerializer

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢全部的使用者個人資料',
    operation_description=""
)
@api_view(['GET'])
def getAllProfile(request):
    all_profile = profile.objects.all()
    serializer = ProfileSerializer(all_profile, many=True)

    if (serializer.data == []):
        return Response({ "message": "Profile not found." }, status=404)
    else:
        return Response(serializer.data)
        

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢指定id的使用者個人資料',
    operation_description="輸入id，查詢使用者個人資料"
)
@api_view(['GET'])
def getProfileById(request, id):
    try:
        p = profile.objects.get(id=id)
        serializer = ProfileSerializer(p)
        return Response(serializer.data, status=200)
    except profile.DoesNotExist:
        return Response({ "message": "Profile not found."}, status=404)
    
@swagger_auto_schema(
    methods=['POST'],
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
    )
)
@api_view(['POST'])
def addProfile(request):

    try:
        rUser = users.objects.get(id=request.data['userID'])
    except users.DoesNotExist:
        return Response({ "message:" "Can't find userId" }, status=404)
    
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
        return Response(serializer.data)
    else:
        return Response({ "message": "Profile format error." }, status=400)
    
@swagger_auto_schema(
    methods=['PUT'],
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
    )
)
@api_view(['PUT'])
def updateProfile(request, id):
    try:
        updateProfile = profile.objects.get(id=id)
    except profile.DoesNotExist:
        return Response({ "update": False, "message": "Profile not found."}, status=404)
    
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
        return Response({ "message": "Profile format error." }, status=400)

@swagger_auto_schema(
    methods=['DELETE'],
    operation_summary='刪除指定id的使用者個人資料',
    operation_description="輸入id，刪除使用者個人資料"
)
@api_view(['DELETE'])
def deleteProfile(request, id):
    try:
        delProfile = profile.objects.get(id=id)
    except profile.DoesNotExist:
        return Response({ "delete": False, "message": "Profile not found." }, status=404)
    
    delProfile.delete()
    return Response({ "delete": True, "message": "Profile deleted successfully." }, status=200)