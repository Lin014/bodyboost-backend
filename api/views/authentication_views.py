from django.utils import timezone

import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Users, EmailVerifyCode
from ..serializers import UsersSerializer
from ..utils.sendMail import sendRegisterMail
from ..utils.response import *
from .user_views import updateUserStatus

@swagger_auto_schema(
    methods=['POST'],
    tags=["Authentication"],
    operation_summary="重寄註冊驗證信",
    operation_description="只限一般使用者",
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
            200: '{ "message": "Send successfully.", "user": UsersObject }',
            404: str(NotFoundResponse('User'))
    }
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def resendRegisterMail(request):
    try:
        user = Users.objects.get(account=request.data['account'], created_type='normal')
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    sendRegisterMail(user.email, user)
    serializer = UsersSerializer(user)
    return Response({ "message": "Send successfully.", "user": serializer.data }, status=200)
    
@swagger_auto_schema(
    methods=['POST'],
    tags=["Authentication"],
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
            200: '{ "message": "Send successfully.", "user": UsersObject }',
            404: str(NotFoundResponse('User'))
    }
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def sendForgetPasswordMail(request):
    try:
        user = Users.objects.get(account=request.data['account'], created_type='normal')
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    sendForgetPasswordMail(user.email, user)
    serializer = UsersSerializer(user)
    return Response({ "message": "Send successfully.", "user": serializer.data })

@swagger_auto_schema(
    methods=['POST'],
    tags=["Authentication"],
    operation_summary="驗證註冊驗證碼",
    operation_description="只限一般使用者使用",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Register verification code.'
            ),
            'userID': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='User id.'
            )
        },
    ),
    responses={
            200: '{ "message": "Verified successful.", "user": UserObject }',
            400: '{ "message": "Verified failed." } or { "message": "Verification code has expired." }',
            404: str(NotFoundResponse('EmailVerifyCode'))
    }
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def authenticationRegisterCode(request):
    try:
        emailVerifyCodeList = EmailVerifyCode.objects.filter(user_id=request.data['userID'], send_type='register')
    except EmailVerifyCode.DoesNotExist:
        return Response(NotFoundResponse('EmailVerifyCode'), status=404)
    
    emailVerifyCodeListLength = len(emailVerifyCodeList)
    for i in range(emailVerifyCodeListLength-1):
        emailVerifyCodeList[i].delete()
    
    now = timezone.now()
    minMatchTime = now - datetime.timedelta(minutes=3)

    if (emailVerifyCodeList[emailVerifyCodeListLength-1].created_at >= minMatchTime):
        if (emailVerifyCodeList[emailVerifyCodeListLength-1].code == request.data['code']):
            updateUser = updateUserStatus(request.data['userID'], 'verified')
            return Response({ "message": "Verified successful.", "user": updateUser }, status=200)
        else:
            return Response({ "message": "Verified failed." }, status=400)
        
    else:
        return Response({ "message": "Verification code has expired." }, status=400)
    
@swagger_auto_schema(
    methods=['POST'],
    tags=["Authentication"],
    operation_summary="驗證忘記密碼驗證碼",
    operation_description="只限一般使用者使用",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Register verification code.'
            ),
            'userID': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='User id.'
            )
        },
    ),
    responses={
            200: '{ "message": "Verified successful." }',
            400: '{ "message": "Verified failed." } or { "message": "Verification code has expired." }',
            404: str(NotFoundResponse('EmailVerifyCode'))
    }
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def authenticationForgetPasswordCode(request):
    try:
        emailVerifyCodeList = EmailVerifyCode.objects.filter(user_id=request.data['userID'], send_type='forget')
    except EmailVerifyCode.DoesNotExist:
        return Response(NotFoundResponse('EmailVerifyCode'), status=404)
    
    emailVerifyCodeListLength = len(emailVerifyCodeList)
    for i in range(emailVerifyCodeListLength-1):
        emailVerifyCodeList[i].delete()
    
    now = timezone.now()
    minMatchTime = now - datetime.timedelta(minutes=3)

    if (emailVerifyCodeList[emailVerifyCodeListLength-1].created_at >= minMatchTime):
        if (emailVerifyCodeList[emailVerifyCodeListLength-1].code == request.data['code']):
            return Response({ "message": "Verified successful." }, status=200)
        else:
            return Response({ "message": "Verified failed." }, status=400)
        
    else:
        return Response({ "message": "Verification code has expired." }, status=400)

