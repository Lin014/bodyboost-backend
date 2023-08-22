from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from datetime import datetime, timedelta

from ..models import SportRecordWeek
from ..serializers import SportRecordWeekSerializer
from ..utils.response import *

def addSportRecordWeek(userId, startDate):
    time_delta = timedelta(days=7)
    end_date = startDate + time_delta

    newSportRecordWeek = {
        "user_id": userId,
        "start_date": startDate.date(),
        "end_date": end_date.date(),
    }

    serializer = SportRecordWeekSerializer(data=newSportRecordWeek)

    if (serializer.is_valid()):
        serializer.save()
        return serializer.data
    else:
        return "Failed"