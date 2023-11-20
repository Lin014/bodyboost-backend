from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from itertools import chain

from ..models import Achievement
from ..serializers import AchievementSerializer
from ..utils.response import *
from ..swagger.achievement import *
from .pagination_views import paginator
from ..swagger.page import pageManualParameters
from ..data.achievement import achievementList

@swagger_auto_schema(
    methods=['GET'],
    tags=["Achievement"],
    operation_summary='查詢所有成就資料',
    operation_description="",
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllAchievement(request):
    achievements = Achievement.objects.all()

    serializer = AchievementSerializer(achievements, many=True)

    if (serializer.data != []):
        return Response(serializer.data, status=200)
    else:
        return Response(NotFoundResponse("Achievement"), status=404)
