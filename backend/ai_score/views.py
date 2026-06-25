from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import get_recommendations, get_single_score


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    content_type = request.query_params.get('type')
    if content_type not in ('bootcamp', 'job', 'certification', 'competition'):
        return Response({'error': 'type 파라미터가 필요합니다. (bootcamp|job|certification|competition)'}, status=400)

    data = get_recommendations(request.user, content_type)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_score(request):
    content_type = request.query_params.get('type')
    object_id = request.query_params.get('id')

    if content_type not in ('bootcamp', 'job', 'certification', 'competition') or not object_id:
        return Response({'error': 'type, id 파라미터가 필요합니다.'}, status=400)

    try:
        object_id = int(object_id)
    except (ValueError, TypeError):
        return Response({'error': 'id는 정수여야 합니다.'}, status=400)

    data = get_single_score(request.user, content_type, object_id)
    return Response(data)
