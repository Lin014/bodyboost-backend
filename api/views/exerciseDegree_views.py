from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import exercise_degree
from ..serializers import ExerciseDegreeSerializer

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢全部的運動程度資料',
    operation_description=""
)
@api_view(['GET'])
def getAllExerciseDegree(request):
    all_exercise_degree = exercise_degree.objects.all()
    serializer = ExerciseDegreeSerializer(all_exercise_degree, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    methods=['GET'],
    operation_summary='查詢指定id的運動程度資料',
    operation_description="輸入id，查詢運動程度資料"
)
@api_view(['GET'])
def getExerciseDegreeById(request, id):
    try:
        exerciseDegree = exercise_degree.objects.get(id=id)
        serializer = ExerciseDegreeSerializer(exerciseDegree)
        return Response(serializer.data, status=200)
    except exercise_degree.DoesNotExist:
        return Response({ "message": "Exercise Degree not found."}, status=404)

@swagger_auto_schema(
    methods=['POST'],
    operation_summary="添加運動程度資料",
    operation_description="基礎代謝率計算所需資料",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'activity_level': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='活動程度'
            ),
            'factor': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='運動因子'
            )
        }
    )
)
@api_view(['POST'])
def addExerciseDegree(request):

    serializer = ExerciseDegreeSerializer(data=request.data)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({ "message": "Exercise Degree format error." }, status=400)
    
@swagger_auto_schema(
    methods=['PUT'],
    operation_summary="更新運動程度資料",
    operation_description="",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'activity_level': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='活動程度'
            ),
            'factor': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='運動因子'
            ),
        }
    )
)
@api_view(['PUT'])
def updateExerciseDegree(request, id):
    try:
        updateExerciseDegree = exercise_degree.objects.get(id=id)
    except exercise_degree.DoesNotExist:
        return Response({ "update": False, "message": "Exercise Degree not found."}, status=404)
    
    updateExerciseDegree.activity_level = request.data['activity_level']
    updateExerciseDegree.factor = request.data['factor']

    serializer = ExerciseDegreeSerializer(updateExerciseDegree)
    if (serializer.is_valid):
        updateExerciseDegree.save()
        return Response(serializer.data, status=200)
    else:
        return Response({ "message": "Exercise Degree format error." }, status=400)
    
@swagger_auto_schema(
    methods=['DELETE'],
    operation_summary='刪除指定id的運動程度資料',
    operation_description="輸入id，刪除運動程度資料"
)
@api_view(['DELETE'])
def deleteExerciseDegree(request, id):
    try:
        delExerciseDegree = exercise_degree.objects.get(id=id)
    except exercise_degree.DoesNotExist:
        return Response({ "delete": False, "message": "Exercise Degree not found." }, status=404)
    
    delExerciseDegree.delete()
    return Response({ "delete": True, "message": "Exercise Degree deleted successfully." }, status=200)
