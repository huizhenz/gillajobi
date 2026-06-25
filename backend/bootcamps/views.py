from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import (
    Region,
    Skill,
    Bootcamp
)
from .serializers import (
    RegionSerializer,
    SkillSerializer,
    BootcampSerializer,
)

from .service import fetch_bootcamps_service
from django.conf import settings

class BootcampPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


@api_view(['GET'])
def bootcamps_list(request):
    bootcamps = Bootcamp.objects.all()

    paginator = BootcampPagination()
    
    page = paginator.paginate_queryset(bootcamps, request) # 전체 recruitments 쿼리셋에서 15개만 잘라서 반환
    serializer = BootcampSerializer(page, many=True) # 잘라낸 15개짜리 page를 JSON으로 직렬화
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def bootcamp_detail(request, bootcamp_pk):
    bootcamp = get_object_or_404(Bootcamp, pk=bootcamp_pk)
    serializer = BootcampSerializer(bootcamp)
    return Response(serializer.data)



@api_view(['GET'])
def fetch_bootcamps(request):
    page_param = request.query_params.get('page')
    if page_param is not None:
        try:
            page = int(page_param)
        except (ValueError, TypeError):
            page = 1
    else:
        page = None
    result = fetch_bootcamps_service(page=page)
    return Response(result)
