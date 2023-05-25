from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator

from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Users, EmailVerifyCode
from ..serializers import UsersSerializer
from ..utils.sendMail import sendRegisterMail
from ..utils.response import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Users"],
    operation_summary='查詢全部的使用者',
    operation_description="",
    responses={
            200: 'UserObject',
            404: str(NotFoundResponse('User'))
    }
)
@api_view(['GET'])
def getAllUser(request):
    all_user = Users.objects.all()
    serializer = UsersSerializer(all_user, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('User'), status=404)
    else:
        return Response(serializer.data)
    

@swagger_auto_schema(
    methods=['GET'],
    tags=["Users"],
    operation_summary='查詢指定id的使用者',
    operation_description="輸入id，查詢使用者",
    responses={
            200: 'UserObject',
            404: str(NotFoundResponse('User'))
    }
)
@api_view(['GET'])
def getUserById(request, id):
    try:
        user = Users.objects.get(id=id)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=200)
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Users"],
    operation_summary="添加一般使用者",
    operation_description="只適用於一般使用者，Google使用者不可，新增成功會回傳user資料",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'account': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User account'
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User password'
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User email'
            ),
        }
    ),
    responses={
            200: 'UserObject',
            400: '{ "created": False, "message": "Duplicate account and/or password" } or ' + str(FormatErrorResponse('User'))
    }  
)
@api_view(['POST'])
def addUser(request):
    newUser = request.data
    duplicateField = []

    try:
        user = Users.objects.get(account=newUser['account'], created_type='normal')
        duplicateField.append('account')
    except Users.DoesNotExist:
        pass

    try:
        user2 = Users.objects.get(email=newUser['email'], created_type='normal')
        duplicateField.append('email')
        return Response({ "created": False, "message": "Duplicate " + " and ".join(duplicateField) }, status=400)
    except Users.DoesNotExist:
        if 'account' in duplicateField:
            return Response({ "created": False, "message": "Duplicate " + " and ".join(duplicateField) }, status=400)
        else:
            password = request.data['password']
            newUser['password'] = make_password(password)
            newUser['status'] = 'unverified'
            newUser['created_type'] = 'normal'

            serializer = UsersSerializer(data=newUser)
            if (serializer.is_valid()):
                serializer.save()
                sendUser = Users.objects.get(id=serializer.data['id'])
                sendRegisterMail(sendUser.email, sendUser)
                return Response(serializer.data)
            else:
                return Response(FormatErrorResponse('User'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Users"],
    operation_summary="更新使用者資料",
    operation_description="更新一般使用者之密碼與信箱，Google使用者無法更新，也可傳入完整users json",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User password'
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User email'  
            )
        }
    ),
    responses={
            200: 'UserObject',
            400: str(FormatErrorResponse('Email')) + ' or { "message": "User cannot be changed." }',
            404: str(NotFoundResponse('User'))
    }    
)
@api_view(['PUT'])
def updateUser(request, id):
    try:
        updateUser = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    user = request.data
    if (updateUser.created_type == 'normal'):
        updateUser.password = make_password(user['password'])
        updateUser.email = user['email']

        serializer = UsersSerializer(updateUser)
        email_validator = EmailValidator()
        try:
            email_validator(updateUser.email)
            updateUser.save()
            return Response(serializer.data, status=200)
        except:
            return Response(FormatErrorResponse('Email'), status=400)
    else:
        return Response({ "message": "User cannot be changed." }, status=400)
   

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Users"],
    operation_summary='刪除指定id的使用者',
    operation_description="輸入id，刪除使用者",
    responses={
            200: '{ "message": "User deleted successfully." }',
            404: str(NotFoundResponse('User'))
    }    
)
@api_view(['DELETE'])
def deleteUser(request, id):
    try:
        delUser = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    delUser.delete()
    return Response({ "message": "User deleted successfully." }, status=200)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Users"],
    operation_summary="一般使用者登入",
    operation_description="只限一般使用者登入使用，如果登入成功會回傳user資料",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'account': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User account'
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User password'
            ),
        }
    ),
    responses={
            200: 'UserObject',
            400: '{ "message": "Wrong password." }',
            404: str(NotFoundResponse('User'))
    }
)
@api_view(['POST'])
def login_normal(request):
    try:
        user = Users.objects.get(account=request.data['account'], created_type='normal')
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    is_pwd_match = check_password(request.data['password'], user.password)
    if (is_pwd_match):
        loginUser = UsersSerializer(user)
        return Response(loginUser.data)
    else:
        return Response({ "message": "Wrong password." }, status=400) 

@swagger_auto_schema(
    methods=['POST'],
    tags=["Users"],
    operation_summary="Google使用者登入",
    operation_description="只限Google使用者登入使用，如果找得到email則回傳對應的user資料，找不到就新建一個後回傳user資料",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User email'
            )
        }
    ),
    responses={
            200: 'UserObject',
            400: str(FormatErrorResponse('User'))
    }
)
@api_view(['POST'])
def login_google(request):
    try:
        user = Users.objects.get(account=request.data['email'], created_type='google')
        loginUser = UsersSerializer(user)
        return Response(loginUser.data)
    except Users.DoesNotExist:
        newUser = request.data
        newUser['account'] = newUser['email']
        newUser['status'] = 'verified'
        newUser['created_type'] = 'google'

        serializer = UsersSerializer(data=newUser)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(FormatErrorResponse('User'), status=400)
    
def updateUserStatus(id, status):
    updateUser = Users.objects.get(id=id)
    updateUser.status = status
    updateUser.save()
