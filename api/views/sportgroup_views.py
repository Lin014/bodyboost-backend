from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import SportGroup, Users, Sport, SportGroupItem, Setting
from ..serializers import SportGroupSerializer, SportGroupItemSerializer
from ..utils.response import *
from ..swagger.sportgroup import *
from .pagination_views import paginator
from ..swagger.page import pageManualParameters

@swagger_auto_schema(
    methods=['GET'],
    tags=["SportGroup"],
    operation_summary='查詢某個user的全部運動組合',
    operation_description="輸入user id，查詢運動組合，並列出所有運動項目的詳細資料",
    manual_parameters=pageManualParameters,
    responses=getSportGroupByUserIdResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getSportGroupByUserId(request, id):
    try:
        sportGroups = SportGroup.objects.filter(user_id=id)
    except SportGroup.DoesNotExist:
        return Response(NotFoundResponse('SportGroup'), status=404)
    
    if (len(sportGroups) == 0):
        return Response(NotFoundResponse('SportGroup'), status=404)
    
    allSportGroup = SportGroupSerializer(sportGroups, many=True).data
    for sportGroup in allSportGroup:
        try:
            sportGroupItems = SportGroupItem.objects.filter(sport_group_id=sportGroup['id'])
            itemsSerializer = SportGroupItemSerializer(sportGroupItems, many=True)
            sportGroup['items'] = itemsSerializer.data
        except SportGroupItem.DoesNotExist:
            pass

    result_page = paginator.paginate_queryset(allSportGroup, request)
    return Response(result_page, status=200)

@swagger_auto_schema(
    methods=['POST'],
    tags=["SportGroup"],
    operation_summary="添加運動組合",
    operation_description="",
    request_body=addSportGroupRequestBody,
    responses=addSportGroupResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addSportGroup(request):

    # check User
    try:
        user = Users.objects.get(id=request.data['user_id'])
    except Users.DoesNotExist:
        return Response(NotFoundResponse('User'), status=404)
    
    # create SportGroup
    newSportGroup = {
        'name': request.data['name'],
        'rest_time': request.data['rest_time'],
        'user_id': user.id
    }

    # check Sport
    items = request.data['items']
    delItems = []
    if (len(items) != 0):
        for index, item in enumerate(items):
            try:
                sport = Sport.objects.get(id=item['sport_id'])
            except Sport.DoesNotExist:
                delItems.append(index)
    if (len(delItems) != 0):
        for index in delItems:
            del items[index]

    # check format and save SportGroup
    serializer = SportGroupSerializer(data=newSportGroup)
    if (serializer.is_valid()):
        serializer.save()
    else:
        return Response(FormatErrorResponse('SportGroup'), status=400)
    
    sportGroup = serializer.data
    
    # SportGroupItem add sport_group_id
    if (len(items) != 0):
        for item in items:
            item['sport_group_id'] = serializer.data['id']
        
        # check format and save SportGroupItems
        serializerItems= SportGroupItemSerializer(data=items, many=True)
        if(serializerItems.is_valid()):
            serializerItems.save()
            sportGroup['items'] = serializerItems.data
            return Response(sportGroup, status=200)
        else:
            return Response(FormatErrorResponse('SportGroupItem'), status=400)
    else:
        sportGroup['items'] = []
        return Response(sportGroup, status=200)
    
@swagger_auto_schema(
    methods=['PUT'],
    tags=["SportGroup"],
    operation_summary="更新運動組合所有資料",
    operation_description="更新所有運動組合的資料，包含 SportGroupItem",
    request_body=addSportGroupRequestBody,
    responses=updateSportGroupResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateSportGroup(request, id):
    try:
        sportGroup = SportGroup.objects.get(id=id)
    except SportGroup.DoesNotExist:
        return Response(NotFoundResponse('SportGroup'), status=404)

    # delete all SportGroupItem
    try:
        sportGroupItems = SportGroupItem.objects.filter(sport_group_id=id).delete()
    except SportGroupItem.DoesNotExist:
        pass
    
    # check Sport
    items = request.data['items']
    delItems = []
    if (len(items) != 0):
        for index, item in enumerate(items):
            try:
                sport = Sport.objects.get(id=item['sport_id'])
            except Sport.DoesNotExist:
                delItems.append(index)
    if (len(delItems) != 0):
        for index in delItems:
            del items[index]

    sportGroup.name = request.data['name']
    sportGroup.rest_time = request.data['rest_time']
    sportGroup.save()

    serializer = SportGroupSerializer(sportGroup)
    sportGroup_data = serializer.data
        
    # SportGroupItem add sport_group_id
    if (len(items) != 0):
        for item in items:
            item['sport_group_id'] = serializer.data['id']
        
        # check format and save SportGroupItems
        serializerItems= SportGroupItemSerializer(data=items, many=True)
        if(serializerItems.is_valid()):
            serializerItems.save()
            sportGroup_data['items'] = serializerItems.data
            return Response(sportGroup_data, status=200)
        else:
            return Response(FormatErrorResponse('SportGroupItem'), status=400)
    else:
        sportGroup_data['items'] = []
        return Response(sportGroup_data, status=200)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["SportGroup"],
    operation_summary="更新運動組合",
    operation_description="只更新運動組合的資料(name, rest_time，不包含 SportGroupItem",
    request_body=updateOnlySportGroupRequestBody,
    responses=updateOnlySportGroupResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateOnlySportGroup(request, id):
    try:
        sportGroup = SportGroup.objects.get(id=id)
    except SportGroup.DoesNotExist:
        return Response(NotFoundResponse('SportGroup'), status=404)

    sportGroup.name = request.data['name']
    sportGroup.rest_time = request.data['rest_time']
    sportGroup.save()

    serializer = SportGroupSerializer(sportGroup)
    return Response(serializer.data, status=200)
    
@swagger_auto_schema(
    methods=['DELETE'],
    tags=["SportGroup"],
    operation_summary='刪除指定id的運動組合',
    operation_description="輸入id，刪除運動組合",
    responses=deleteSportGroupResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteSportGroup(request, id):
    try:
        delSportGroup = SportGroup.objects.get(id=id)
    except SportGroup.DoesNotExist:
        return Response(NotFoundResponse('SportGroup'), status=404)

    delSportGroup.delete()
    return Response({"message": "SportGroup deleted successfully."}, status=200)

    



