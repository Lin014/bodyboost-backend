from django.contrib.auth.hashers import make_password, check_password

from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import users
from ..serializers import UsersSerializer
from ..utils.sendMail import sendVerificationMail

from django.core.validators import EmailValidator

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢全部的使用者',
    operation_description="",
    responses={
            200: 'userObject',
            404: '{ "message": "User not found." }'
    } 
)
@api_view(['GET'])
def getAllUser(request):
    all_user = users.objects.all()
    serializer = UsersSerializer(all_user, many=True)
    
    if (serializer.data == []):
        return Response({ "message": "User not found." }, status=404)
    else:
        return Response(serializer.data)
    

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢指定id的使用者',
    operation_description="輸入id，查詢使用者",
    responses={
            200: 'userObject',
            404: '{ "message": "User not found." }'
    }  
)
@api_view(['GET'])
def getUserById(request, id):
    try:
        user = users.objects.get(id=id)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=200)
    except users.DoesNotExist:
        return Response({ "message": "User not found." }, status=404)

@swagger_auto_schema(
    methods=['POST'],
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
            200: 'userObject',
            400: '{ "created": False, "message": "Duplicate account and/or password" } or { "message": "User format error." }'
    }   
)
@api_view(['POST'])
def addUser(request):
    newUser = request.data
    duplicateField = []

    try:
        user = users.objects.get(account=newUser['account'], created_type='normal')
        duplicateField.append('account')
    except users.DoesNotExist:
        print('Account is not duplicate.')

    try:
        user2 = users.objects.get(email=newUser['email'], created_type='normal')
        duplicateField.append('email')
        return Response({ "created": False, "message": "Duplicate " + " and ".join(duplicateField) }, status=400)
    except users.DoesNotExist:
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
                sendUser = users.objects.get(id=serializer.data['id'])
                sendVerificationMail(sendUser.email, sendUser)
                return Response(serializer.data)
            else:
                return Response({ "message": "User format error." }, status=400)

@swagger_auto_schema(
    methods=['PUT'],
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
            200: 'userObject',
            400: '{ "message": "Email format error." } or { "update": False, "message": "User cannot be changed." }',
            404: '{ "update": False, "message": "User not found." }'
    }    
)
@api_view(['PUT'])
def updateUser(request, id):
    try:
        updateUser = users.objects.get(id=id)
    except users.DoesNotExist:
        return Response({ "update": False, "message": "User not found."}, status=404)
    
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
            return Response({ "message": "Email format error." }, status=400)
    else:
        return Response({ "update": False, "message": "User cannot be changed." }, status=400)
   

@swagger_auto_schema(
    methods=['DELETE'],
    operation_summary='刪除指定id的使用者',
    operation_description="輸入id，刪除使用者",
    responses={
            200: '{ "delete": True, "message": "User deleted successfully." }',
            404: '{ "delete": False, "message": "User not found." }'
    }    
)
@api_view(['DELETE'])
def deleteUser(request, id):
    try:
        delUser = users.objects.get(id=id)
    except users.DoesNotExist:
        return Response({ "delete": False, "message": "User not found." }, status=404)
    
    delUser.delete()
    return Response({ "delete": True, "message": "User deleted successfully." }, status=200)

@swagger_auto_schema(
    methods=['POST'],
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
            200: 'userObject',
            400: '{ "login": False, "message": "Wrong password."}',
            404: '{ "message": "User not found." }'
    }
)
@api_view(['POST'])
def login_normal(request):
    try:
        user = users.objects.get(account=request.data['account'], created_type='normal')
    except users.DoesNotExist:
        return Response({ "message": "User not found." }, status=404)
    
    is_pwd_match = check_password(request.data['password'], user.password)
    if (is_pwd_match):
        loginUser = UsersSerializer(user)
        return Response(loginUser.data)
    else:
        return Response({ "login": False, "message": "Wrong password."}, status=400)    

@swagger_auto_schema(
    methods=['POST'],
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
            200: 'userObject',
            400: '{ "message": "User format error." }'
    }
)
@api_view(['POST'])
def login_google(request):
    try:
        user = users.objects.get(account=request.data['email'], created_type='google')
        loginUser = UsersSerializer(user)
        return Response(loginUser.data)
    except users.DoesNotExist:
        newUser = request.data
        newUser['account'] = newUser['email']
        newUser['status'] = 'verified'
        newUser['created_type'] = 'google'

        serializer = UsersSerializer(data=newUser)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({ "message": "User format error." }, status=400)

@swagger_auto_schema(
    methods=['GET'],
    operation_summary="重寄註冊驗證信",
    operation_description="只限一般使用者",
    responses={
            200: '{ "message": "Send successfully." }',
            404: '{ "message": "User not found." }'
    }
)
@api_view(['GET'])
def resendVerificationMail(request, id):
    try:
        user = users.objects.get(id=id)
    except users.DoesNotExist:
        return Response({ "message": "User not found." }, status=404)
    
    sendVerificationMail(user.email, user)
    return Response({ "message": "Send successfully." }, status=200)
    
@swagger_auto_schema(
    methods=['POST'],
    operation_summary="寄送忘記密碼驗證信",
    operation_description="只限一般使用者使用",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'account': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User account'
            )
        },
    ),
    responses={
            200: '{ "message": "Send successfully.", "user": userObject }',
            404: '{ "message": "User not found." }'
    }
)
@api_view(['POST'])
def sendForgetPasswordMail(request):
    try:
        user = users.objects.get(account=request.data['account'], created_type='normal')
    except users.DoesNotExist:
        return Response({ "message": "User not found." }, status=404)
    
    sendForgetPasswordMail(user.email, user)
    serializer = UsersSerializer(user)
    return Response({ "message": "Send successfully.", "user": serializer.data })

