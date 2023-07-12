from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import DailyBonus, Users
from ..serializers import DailyBonusSerializer
from ..utils.response import *
from ..swagger.dailybonus import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["DailyBonus"],
    operation_summary='查詢指定使用者簽到記錄',
    operation_description="輸入id，查詢使用者簽到記錄",
    responses=getDailyBonusByIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getDailyBonusById(request, id):
    try:
        all_dailyBonus = DailyBonus.objects.filter(user_id=id)
        serializer = DailyBonusSerializer(all_dailyBonus, many=True)
        return Response(serializer.data, status=200)
    except DailyBonus.DoesNotExist:
        return Response(NotFoundResponse('DailyBonus'), status=404)

@swagger_auto_schema(
    methods=['POST'],
    tags=["DailyBonus"],
    operation_summary="添加簽到記錄",
    operation_description="",
    responses=addDailyBonusByIdResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addDailyBonusById(request, id):
    try:
        user = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    all_dailyBonus = DailyBonus.objects.filter(user_id=id).order_by('date')
    now = timezone.now()

    print(all_dailyBonus.count())

    if (all_dailyBonus.count() != 0):
        if now.date() == all_dailyBonus[0].date.date():
            return Response({ "message": 'This account was signed in today.'}, status=400)

    newDailyBonus = {
        "user_id": id
    }

    serializer = DailyBonusSerializer(data=newDailyBonus)

    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(FormatErrorResponse('DailyBonus'), status=400)