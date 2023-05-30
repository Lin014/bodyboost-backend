from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Store
from ..serializers import StoreSerializer
from ..utils.response import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Store"],
    operation_summary='查詢全部商店資料',
    operation_description="",
    responses={
            200: StoreSerializer,
            404: str(NotFoundResponse('Store'))
    }
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAllStore(request):
    all_store = Store.objects.all()
    serializer = StoreSerializer(all_store, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Store'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Store"],
    operation_summary="添加商店資料",
    operation_description="",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='商店名稱'
            )
        }
    ),
    responses={
            200: StoreSerializer,
            400: '{ "message": "Store already exists.", "store": StoreObject }'
    }
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addStore(request):

    try:
        oStore = Store.objects.get(name=request.data['name'])
        return Response({ "message": "Store already exists.", "store": oStore }, status=400)
    except Store.DoesNotExist:
        newStore = Store.objects.create(name=request.data['name'])
        serializer = StoreSerializer(newStore)
        return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Store"],
    operation_summary="更新商店資料",
    operation_description="",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='商店名稱'
            ),
        }
    ),
    responses={
            200: StoreSerializer,
            404: str(NotFoundResponse('Store'))
    }
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateStore(request, id):
    try:
        updateStore = Store.objects.get(id=id)
    except Store.DoesNotExist:
        return Response(NotFoundResponse('Store'), status=404)
    
    updateStore.name = request.data['name']
    updateStore.save()

    serializer = StoreSerializer(updateStore)
    return Response(serializer.data, status=200)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Store"],
    operation_summary='刪除指定id的商店資料',
    operation_description="輸入id，刪除商店資料",
    responses={
            200: '{ "message": "Store deleted successfully." }',
            404: str(NotFoundResponse('Store'))
    }
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteStore(request, id):
    try:
        delStore = Store.objects.get(id=id)
    except Store.DoesNotExist:
        return Response(NotFoundResponse('Store'), status=404)
    
    delStore.delete()
    return Response({ "message": "Store deleted successfully." }, status=200)

