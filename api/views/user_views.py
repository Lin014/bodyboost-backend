from django.contrib.auth.hashers import make_password, check_password

from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import users
from ..serializers import UsersSerializer

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢全部的使用者',
    operation_description=""
)
@api_view(['GET'])
def getUsers(request):
    all_user = users.objects.all()
    serializer = UsersSerializer(all_user, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢指定id的使用者',
    operation_description="輸入id，查詢使用者"
)
@api_view(['GET'])
def getUserById(request, id):
    try:
        user = users.objects.get(id=id)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=200)
    except users.DoesNotExist:
        return Response({ "message": "User not found."}, status=404)

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
    )
)
@api_view(['POST'])
def addUser(request):
    newUser = request.data
    password = request.data['password']
    newUser['password'] = make_password(password)
    newUser['status'] = 'unverified'
    newUser['created_type'] = 'normal'

    serializer = UsersSerializer(data=newUser)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({ "message": "User format error." }, status=400)

@swagger_auto_schema(
    methods=['PUT'],
    operation_summary="更新使用者資料",
    operation_description="不管是一般或Google使用者都可更新，不過一般使用者能更改的欄位只有password、status，Google使用者只有status，也可傳完整的user欄位。修改成功後會回傳修改後的user資料",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User password'
            ),
            'status': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User status'
            ),
        }
    )
)
@api_view(['PUT'])
def updateUser(request, id):
    try:
        updateUser = users.objects.get(id=id)
    except users.DoesNotExist:
        return Response({ "update": False, "message": "User not found."}, status=404)
    
    user = request.data
    if (user['created_type'] == 'normal'):
        updateUser.password = make_password(user['password'])
        updateUser.status = user['status']
        
    else:
        updateUser.status = user['status']

    updateUser.save()

    serializer = UsersSerializer(updateUser)
    return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['DELETE'],
    operation_summary='刪除指定id的使用者',
    operation_description="輸入id，刪除使用者"
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
    )
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
                description='User account'
            )
        }
    )
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

