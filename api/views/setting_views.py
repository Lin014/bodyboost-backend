from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import Setting, Users
from ..serializers import SettingSerializer, UsersSerializer
from ..utils.sendMail import sendRegisterMail
from ..utils.response import *
from ..swagger.setting import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Setting"],
    operation_summary='查詢指定使用者之設定資料',
    operation_description="",
    responses=getSettingByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getSettingByUserId(request, id):
    try:
        setting = Setting.objects.get(user_id=id)
        serializer = SettingSerializer(setting)

        return Response(serializer.data, status=200)
    except Setting.DoesNotExist:
        return Response(NotFoundResponse('Setting'), status=404)

def addSetting(userId):
    newSetting = {
        'theme': 'light',
        'anim_char_name': 'Bob',
        'is_alerted': False,
        'user_id': userId
    }

    serializer = SettingSerializer(data=newSetting)
    if (serializer.is_valid()):
        serializer.save()
    else:
        return Response(FormatErrorResponse('Setting'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Setting"],
    operation_summary="更新設定資料",
    operation_description="",
    request_body=updateSettingRequestBody,
    responses=updateSettingResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateSetting(request, id):
    try:
        updateSetting = Setting.objects.get(id=id)
        try:
            updateSetting.theme = request.data['theme']
            updateSetting.anim_char_name = request.data['anim_char_name']
            updateSetting.is_alerted = request.data['is_alerted']
            if (request.data['is_alerted']):
                updateSetting.alert_day = request.data['alert_day']
                updateSetting.alert_time = request.data['alert_time']
            updateSetting.save()
            serializer = SettingSerializer(updateSetting)
            return Response(serializer.data, status=200)
        except:
            return Response(FormatErrorResponse('Setting'), status=400)
    except Setting.DoesNotExist:
        return Response(NotFoundResponse('Setting'), status=404)