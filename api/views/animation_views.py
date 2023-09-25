from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..models import Sport, Animation
from ..serializers import AnimationSerializer
from ..utils.response import *
from ..utils.validate import validateImage, validateVideo
from ..swagger.animatedcharacter import *

@swagger_auto_schema(
    methods=['GET'],
    tags=["Animation"],
    operation_summary='查詢全部動畫',
    operation_description="",
    responses=getAnimationResponses
)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAnimation(request):
    animation = Animation.objects.all()
    serializer = AnimationSerializer(animation, many=True)

    if (serializer.data == []):
        return Response(NotFoundResponse('Animation'), status=404)
    else:
        return Response(serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    tags=["Animation"],
    operation_summary="添加動畫",
    operation_description="",
    request_body=addAnimationRequestBody,
    responses=addAnimationResponses
)
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addAnimation(request):
    try:
        sport = Sport.objects.get(id=request.data['sport_id'])
    except Sport.DoesNotExist:
        return Response(NotFoundResponse('Sport'), status=404)

    name = request.data['name']
    animation = request.data['animation']
    image = request.data['image']
    sport_id = request.data['sport_id']

    if (validateVideo(animation)):
        if (validateImage(image)):

            newAnimation = Animation.objects.create(name=name, sport_id=sport, animation=animation, image=image)
            serializer = AnimationSerializer(newAnimation)
            return Response(serializer.data, status=200)

            # newAnimation = {
            #     'name': name,
            #     'animation': animation,
            #     'image': image,
            #     'sport_id': sport_id
            # }

            # serializer = AnimationSerializer(data=newAnimation)

            # if (serializer.is_valid()):
            #     serializer.save()
            #     return Response(serializer.data, status=200)
            # else:
            #     print(serializer.errors)
            #     return Response(FormatErrorResponse('Animation'), status=400)
        else:
            return Response(FormatErrorResponse("Animation's image"), status=400)
    else:
        return Response(FormatErrorResponse("Animation's animation"), status=400)

@swagger_auto_schema(
    methods=['PUT'],
    tags=["Animation"],
    operation_summary="更新動畫資料",
    operation_description="",
    request_body=addAnimationRequestBody,
    responses=addAnimationResponses
)
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateAnimation(request, id):
    try:
        updateAnimation = Animation.objects.get(id=id)

        name = request.data['name']
        animation = request.data['animation']
        image = request.data['image']

        if (validateVideo(animation)):
            if (validateImage(image)):
                updateAnimation.name = name
                updateAnimation.animation = animation
                updateAnimation.image = image

                updateAnimation.save()

                serializer = AnimationSerializer(updateAnimation)
                return Response(serializer.data, status=200)
            else:
                return Response(FormatErrorResponse("Animation's image"), status=400)
        else:
            return Response(FormatErrorResponse("Animation's animation"), status=400)
    except Animation.DoesNotExist:
        return Response(NotFoundResponse('Animation'), status=404)

@swagger_auto_schema(
    methods=['DELETE'],
    tags=["Animation"],
    operation_summary='刪除指定id的動畫',
    operation_description="輸入id，刪除動畫",
    responses=deleteAnimationResponses
)
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteAnimation(request, id):
    try:
        delAnimation = Animation.objects.get(id=id)
    except Animation.DoesNotExist:
        return Response(NotFoundResponse('Animation'), status=404)

    delAnimation.delete()
    return Response({"message": "Animation deleted successfully."}, status=200)

    