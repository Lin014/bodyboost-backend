from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import SportFrequency, Sport
from ..serializers import SportFrequencySerializer
from ..utils.response import *
from ..swagger.sportfrequency import *
from .pagination_views import paginator
from ..swagger.page import pageManualParameters

@swagger_auto_schema(
    methods=['GET'],
    tags=["SportFrequency"],
    operation_summary='查詢全部運動頻率，呈運動頻率遞減排序',
    operation_description="",
    manual_parameters=pageManualParameters,
    responses=getAllSportFrequencyResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllSportFrequency(request):
    all_sport_frequency = SportFrequency.objects.all().order_by('-frequency')
    result_page = paginator.paginate_queryset(all_sport_frequency, request)
    serializer = SportFrequencySerializer(result_page, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('SportFrequency'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    tags=["SportFrequency"],
    operation_summary="增加運動項目使用次數",
    operation_description="",
    request_body=addSportFrequencyRequestBody,
    responses=addSportFrequencyResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addSportFrequency(request):
    try:
        sport = Sport.objects.get(id=request.data['sport_id'])
    except Sport.DoesNotExist:
        return Response(NotFoundResponse('Sport'), status=404)

    try:
        sportFrequency = SportFrequency.objects.get(sport=request.data['sport_id'])
        sportFrequency.frequency += 1
        sportFrequency.save()
        return Response({ 'message': 'Add Successfully.'}, status=200)
    except SportFrequency.DoesNotExist:
        print('does not exist')
        newSportFrequency = {
            'frequency': 1,
            'sport': request.data['sport_id']
        }

        newSportFrequency['frequency'] = 1

        serializer = SportFrequencySerializer(data=newSportFrequency)
        if (serializer.is_valid()):
            serializer.save()
            return Response({ 'message': 'Add Successfully.'}, status=200)
        else:
            return Response(FormatErrorResponse('SportFrequency'), status=400)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["SportFrequency"],
    operation_summary='刪除指定id的運動項目使用次數',
    operation_description="輸入id，刪除運動項目使用次數",
    responses=deleteSportFrequencyResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteSportFrequency(request, id):
    try:
        delSportFrequency = SportFrequency.objects.get(id=id)
    except SportFrequency.DoesNotExist:
        return Response(NotFoundResponse('SportFrequency'), status=404)

    delSportFrequency.delete()
    return Response({"message": "SportFrequency deleted successfully."}, status=200)

