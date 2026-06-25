from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Competition
from .serializers import CompetitionSerializer
from .services import run_sync

class CompetitionPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


# Create your views here.
@api_view(['GET'])
def competitions_top3(request):
    top3 = (
        Competition.objects
        .order_by('-view_count')
        .values('id', 'title', 'host', 'view_count')[:3]
    )
    return Response(list(top3))


@api_view(['GET'])
def fetch_competitions(request):
    competitions = Competition.objects.all()
    paginator = CompetitionPagination()
    
    page = paginator.paginate_queryset(competitions, request) # 전체 recruitments 쿼리셋에서 15개만 잘라서 반환
    serializer = CompetitionSerializer(page, many=True) # 잘라낸 15개짜리 page를 JSON으로 직렬화
    return paginator.get_paginated_response(serializer.data) # 페이지 정보도 같이 감싸서 반환


@api_view(['POST'])
def sync_competitions(request):
    total_saved = run_sync()
    return Response({"saved": total_saved}, status=status.HTTP_200_OK)


@api_view(['GET'])
def fetch_competition_detail(request, pk):
    competitions = Competition.objects.get(pk=pk)
    Competition.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
    serializer = CompetitionSerializer(competitions)
    return Response(serializer.data, status=status.HTTP_200_OK)
