from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import Member
from ..serializers import MemberSerializer
from ..utils.response import *
from ..swagger.member import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Member"],
    operation_summary='查詢某個使用者的會員資料',
    operation_description="輸入user id查詢",
    responses=getMemberByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getMemberByUserId(request, id):
    try:
        member = Member.objects.get(user_id=id)
        serializer = MemberSerializer(member)
        
        return Response(serializer.data, status=200)
    except Member.DoesNotExist:
        return Response(NotFoundResponse('Member'), status=404)

def addMember(userId):
    newMember = {
        'user_id': userId,
    }

    serializer = MemberSerializer(data=newMember)
    if (serializer.is_valid()):
        serializer.save()
    else:
        return Response(FormatErrorResponse('Member'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Member"],
    operation_summary='更新某個使用者的會員資料',
    operation_description="輸入 user id 更新",
    request_body=updateMemberRequestBody,
    responses=updateMemberResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateMember(request, id):
    try:
        member = Member.objects.get(user_id=id)
        member.member_type = request.data['member_type']
        member.phone = request.data['phone']
        member.is_trial = request.data['is_trial']
        member.payment_type = request.data['payment_type']
        member.save()
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=200)
    except Member.DoesNotExist:
        return Response(NotFoundResponse('Member'), status=404)
    