from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import DietDayRecord
from ..serializers import DietDayRecordSerializer
from ..utils.response import *

def addDietDayRecord(user_id):
    newDietDayRecord = { "user_id": user_id, }
    serializer = DietDayRecordSerializer(data=newDietDayRecord)
    if (serializer.is_valid()):
        serializer.save()
        return "SuccessFully"
    else:
        return "Failed"