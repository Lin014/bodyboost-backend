from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import users
from .serializers import UsersSerializer
# Create your views here.

@api_view(['GET'])
def getUsers(request):
    all_user = users.objects.all()
    serializer = UsersSerializer(all_user, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addUser(request):
    newUser = request.data.copy()
    newUser['status'] = 'unverified'
    newUser['created_type'] = 'normal'

    serializer = UsersSerializer(data=newUser)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({ 'message': 'error format' })