from django.contrib.auth.hashers import make_password, check_password

from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import users
from ..serializers import UsersSerializer

@api_view(['GET'])
def getUsers(request):
    all_user = users.objects.all()
    serializer = UsersSerializer(all_user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserById(request, id):
    try:
        user = users.objects.get(id=id)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=200)
    except users.DoesNotExist:
        return Response({ "message": "User not found."}, status=404)

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

@api_view(['DELETE'])
def deleteUser(request, id):
    try:
        delUser = users.objects.get(id=id)
    except users.DoesNotExist:
        return Response({ "delete": False, "message": "User not found." }, status=404)
    
    delUser.delete()
    return Response({ "delete": True, "message": "User deleted successfully." }, status=200)

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