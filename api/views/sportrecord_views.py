from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from ..models import SportRecord, SportRecordItem, Sport, Users, SportGroup, SportGroupItem
from ..serializers import SportRecordSerializer, SportRecordItemSerializer
from ..utils.response import *
from ..swagger.sportrecord import *
from ..utils.validate import validateVideo
from .pagination_views import paginator
from ..swagger.page import pageManualParameters
from ..views.sportfrequency_views import addSportFrequencyList
from ..views.achievementrecord_veiws import addUserAchievedSport, checkUnlockSportAchievedment

@swagger_auto_schema(
    methods=['GET'],
    tags=["SportRecord"],
    operation_summary='查詢某個user的全部運動紀錄',
    operation_description="輸入user id，查詢運動紀錄",
    manual_parameters=pageManualParameters,
    responses=getSportRecordByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getSportRecordByUserId(request, id):
    try:
        sportRecords = SportRecord.objects.filter(user_id=id)
    except SportRecord.DoesNotExist:
        return Response(NotFoundResponse('SportRecord'), status=404)
    
    if (len(sportRecords) == 0):
        return Response(NotFoundResponse('SportRecord'), status=404)
    
    allSportRecord = SportRecordSerializer(sportRecords, many=True).data
    for sportRecord in allSportRecord:
        try:
            sportRecordItems = SportRecordItem.objects.filter(sport_record_id=sportRecord['id'])
            itemsSerializer = SportRecordItemSerializer(sportRecordItems, many=True)
            sportRecord['items'] = itemsSerializer.data
        except SportRecordItem.DoesNotExist:
            pass
    
    result_page = paginator.paginate_queryset(allSportRecord, request)
    return Response(result_page, status=200)

@swagger_auto_schema(
    methods=['POST'],
    tags=["SportRecord"],
    operation_summary="添加運動紀錄，按下開始運動即要添加",
    operation_description="",
    request_body=addSportRecordRequestBody,
    responses=addSportRecordResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addSportRecord(request):
    # check user
    try:
        user = Users.objects.get(id=request.data['user_id'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    try:
        if (request.data['type'] == 'single'):
            try:
                sport = Sport.objects.get(id=request.data['sport_id'])
            except Sport.DoesNotExist:
                return Response(NotFoundResponse('Sport'), status=404)

            newSportRecord = {
                'type': request.data['type'],
                'is_record_video': request.data['is_record_video'],
                'user_id': request.data['user_id'],
            }

            sportRecordSerializer = SportRecordSerializer(data=newSportRecord)
            if (sportRecordSerializer.is_valid()):
                sportRecordSerializer.save()
            else:
                return Response(FormatErrorResponse('SportRecord'), status=400)
            
            newSportRecordItem = {
                'sport_id': sport.id,
                'no': 1,
                'mode': request.data['mode'],
                'sport_record_id': sportRecordSerializer.data['id']
            }

            if (request.data['mode'] == 'timing'):
                newSportRecordItem['custom_time'] = request.data['custom_time']
            elif (request.data['mode'] == 'counting'):
                newSportRecordItem['custom_counts'] = request.data['custom_counts']
            
            sportRecordItemSerializer = SportRecordItemSerializer(data=newSportRecordItem)
            if (sportRecordItemSerializer.is_valid()):
                sportRecordItemSerializer.save()

                sportRecord = sportRecordSerializer.data
                sportRecord['item'] = sportRecordItemSerializer.data

                return Response(sportRecord, status=200)
            else:
                return Response(FormatErrorResponse('SportRecordItem'), status=400)
        elif (request.data['type'] == 'combo'):
            sportGroup = SportGroup.objects.get(id=request.data['sport_group_id'])
            sportGroupItems = SportGroupItem.objects.filter(sport_group_id=request.data['sport_group_id'])

            if (len(sportGroupItems) == 0):
                return Response(NotFoundResponse('SportGroupItem'), status=404)

            newSportRecord = {
                'rest_time': sportGroup.rest_time,
                'type': request.data['type'],
                'is_record_video': request.data['is_record_video'],
                'user_id': request.data['user_id'],
                'sport_group_id': sportGroup.id,
            }

            sportRecordSerializer = SportRecordSerializer(data=newSportRecord)
            if (sportRecordSerializer.is_valid()):
                sportRecordSerializer.save()
            else:
                return Response(FormatErrorResponse('SportRecord'), status=400)
            
            sportRecordItems = []
            for sportGroupItem in sportGroupItems:
                sport = sportGroupItem.sport_id
                sportRecordItems.append({
                    'sport_id': sport.id,
                    'custom_time': sportGroupItem.custom_time,
                    'custom_counts': sportGroupItem.custom_counts,
                    'no': sportGroupItem.no,
                    'mode': sportGroupItem.mode,
                    'sport_record_id': sportRecordSerializer.data['id']
                })

            sportRecordItemSerializer = SportRecordItemSerializer(data=sportRecordItems, many=True)
            if (sportRecordItemSerializer.is_valid()):
                sportRecordItemSerializer.save()

                sportRecord = sportRecordSerializer.data
                sportRecord['items'] = sportRecordItemSerializer.data

                return Response(sportRecord, status=200)
            else:
                return Response(FormatErrorResponse('SportRecordItem'), status=400)      
        else:
            return Response(FormatErrorResponse('SportRecord'), status=400)
        
    except SportGroup.DoesNotExist:
        return Response(NotFoundResponse('SportGroup'), status=404)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["SportRecord"],
    operation_summary="更新運動紀錄項目 (SportRecordItem)",
    operation_description="輸入sportRecordItem id當運動項目做完時即要更新",
    request_body=updateSportRecordItemRequestBody,
    responses=updateSportRecordItemResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateSportRecordItem(request, id):
    try:
        sportRecordItem = SportRecordItem.objects.get(id=id)
    except:
        return Response(NotFoundResponse('SportRecordItem'), status=404)
    
    sportRecordItem.time = request.data['time']
    sportRecordItem.counts = request.data['counts']
    sportRecordItem.consumed_kcal = request.data['consumed_kcal']
    sportRecordItem.save()
        
    sportRecord = SportRecord.objects.get(id=sportRecordItem.sport_record_id.id)
    sportRecord.cur_sport_no = sportRecordItem.no
    sportRecord.total_consumed_kcal += sportRecordItem.consumed_kcal
    sportRecord.total_time += sportRecordItem.time

    sportRecordItemCount = SportRecordItem.objects.filter(sport_record_id=sportRecord.id).count()
    if (sportRecordItem.no == sportRecordItemCount):
        sportRecord.end_time = timezone.now()
        sportRecord.is_completed = True
    
    sportRecord.save()
    sportRecordItemSerializer = SportRecordItemSerializer(sportRecordItem)

    addSportFrequencyList([sportRecordItem.sport_id])
    addUserAchievedSport(sportRecordItem.sport_record_id.user_id.id, [sportRecordItem.sport_id])
    checkResult = checkUnlockSportAchievedment(sportRecordItem.sport_record_id.user_id)
    result = [
        sportRecordItemSerializer.data,
        { 
            "checkResult": checkResult
        }
    ]
    return Response(result, status=200)


@swagger_auto_schema(
    methods=['DELETE'],
    tags=["SportRecord"],
    operation_summary='刪除指定id的運動紀錄',
    operation_description="輸入id，刪除運動紀錄",
    responses=deleteSportRecordResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteSportRecord(request, id):
    try:
        delSportRecord = SportRecord.objects.get(id=id)
    except SportRecord.DoesNotExist:
        return Response(NotFoundResponse('SportRecord'), status=404)

    delSportRecord.delete()
    return Response({"message": "SportRecord deleted successfully."}, status=200)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["SportRecordItem"],
    operation_summary="上傳運動項目紀錄影片",
    operation_description="輸入運動項目 id，並上傳影片",
    request_body=uploadSportRecordItemVideoRequestBody,
    responses=uploadSportRecordItemVideoResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def uploadSportRecordItemVideo(request, id):
    try:
        sportRecordItem = SportRecordItem.objects.get(id=id)

        video = request.data['video']

        if (validateVideo(video)):
            sportRecordItem.video = video
            sportRecordItem.save()
            serializer = SportRecordItemSerializer(sportRecordItem)
            return Response(serializer.data, status=200)
        else:
            return Response(FormatErrorResponse('Video'), status=400)
    except SportRecordItem.DoesNotExist:
        return Response(NotFoundResponse('SportRecordItem'), status=404)

@swagger_auto_schema(
    methods=['GET'],
    tags=["SportRecord"],
    operation_summary='查詢某個user的近期五筆運動紀錄',
    operation_description="輸入user id，查詢近期運動紀錄",
    responses=getSportRecordByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getLatestSportRecordByUserId(request, id):
    try:
        sportRecords = SportRecord.objects.filter(user_id=id).order_by('-start_time')[:5]
    except SportRecord.DoesNotExist:
        return Response(NotFoundResponse('SportRecord'), status=404)
    
    if (len(sportRecords) == 0):
        return Response(NotFoundResponse('SportRecord'), status=404)
    
    allSportRecord = SportRecordSerializer(sportRecords, many=True).data
    for sportRecord in allSportRecord:
        try:
            sportRecordItems = SportRecordItem.objects.filter(sport_record_id=sportRecord['id'])
            itemsSerializer = SportRecordItemSerializer(sportRecordItems, many=True)
            sportRecord['items'] = itemsSerializer.data
        except SportRecordItem.DoesNotExist:
            pass

    return Response(allSportRecord, status=200)