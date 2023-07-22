from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import Sport, Animation, Setting
from ..serializers import SportSerializer, AnimationSerializer
from ..utils.response import *
from ..swagger.sport import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Sport"],
    operation_summary='查詢指定使用者的全部運動項目',
    operation_description="使用者如果是Premium會員就能享有更換動畫人物的資格，所以需輸入使用者id去識別他是哪個動畫人物",
    responses=getAllSportByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllSportByUserId(request, id):
    all_sport = Sport.objects.all()
    serializer = SportSerializer(all_sport, many=True)

    sportlist = serializer.data
    setting = Setting.objects.get(user_id=id)
    for sport in sportlist:
        try:
            animation = Animation.objects.get(sport_id=sport['id'], name=setting.anim_char_name)
            ainmationSerializer = AnimationSerializer(animation)
            sport['animation'] = ainmationSerializer.data
        except Animation.DoesNotExist:
            sport['animation'] = {}

    if (serializer.data == []):
        return Response(NotFoundResponse('Sport'), status=404)
    else:
        return Response(sportlist)
    
@swagger_auto_schema(
    methods=['POST'],
    tags=["Sport"],
    operation_summary='查詢指定sport id和user id的運動項目',
    operation_description="使用者如果是Premium會員就能享有更換動畫人物的資格，所以需輸入使用者id去識別他是哪個動畫人物",
    request_body=getSportByIdAndUserIdRequestBody,
    responses=getSportByIdAndUserIdResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getSportByIdAndUserId(request):
    try:
        sport = Sport.objects.get(id=request.data['sport_id'])
        serializer = SportSerializer(sport)

        setting = Setting.objects.get(user_id=request.data['user_id'])
        resultSport = serializer.data
        try:
            animation = Animation.objects.get(sport_id=request.data['sport_id'], name=setting.anim_char_name)
            animationSerializer = AnimationSerializer(animation)
            resultSport['animation'] = animationSerializer.data
        except:
            resultSport['animation'] = {}

        return Response(resultSport, status=200)
    except Sport.DoesNotExist:
        return Response(NotFoundResponse('Sport'), status=404)
    

@swagger_auto_schema(
    methods=['POST'],
    tags=["Sport"],
    operation_summary="添加運動項目",
    operation_description="",
    request_body=addSportRequestBody,
    responses=addSportResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addSport(request):
    newSport = request.data

    serializer = SportSerializer(data=newSport)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(FormatErrorResponse('Sport'), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Sport"],
    operation_summary="更新運動項目",
    operation_description="",
    request_body=addSportRequestBody,
    responses=updateSportResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateSport(request, id):
    try:
        updateSport = Sport.objects.get(id=id)
    except Sport.DoesNotExist:
        return Response(NotFoundResponse('Sport'), status=404)
    
    updateSport.name = request.data['name']
    updateSport.description = request.data['description']
    updateSport.default_time = request.data['default_time']
    updateSport.interval = request.data['interval']
    updateSport.is_count = request.data['is_count']
    updateSport.met = request.data['met']
    updateSport.save()

    serializer = SportSerializer(updateSport)
    return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Sport"],
    operation_summary='刪除指定id的運動項目',
    operation_description="輸入id，刪除運動項目",
    responses=deleteSportResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteSport(request, id):
    try:
        delSport = Sport.objects.get(id=id)
    except Sport.DoesNotExist:
        return Response(NotFoundResponse('Sport'), status=404)

    delSport.delete()
    return Response({"message": "Sport deleted successfully."}, status=200)

