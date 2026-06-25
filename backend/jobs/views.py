from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import (
    Company,
    Recruitment,
    RecruitmentDetail,
    HiringProcess,
)
from .serializers import (
    CompanySerializer,
    HiringProcessSerializer,
    RecruitmentDetailSerializer,
    RecruitmentListSerializer,
    RecruitmentDetailReadSerializer
)

from .service import fetch_jobs_service, fetch_detail_service

class JobPagination(PageNumberPagination):
    page_size = 15 # 3열 그리드에 맞춰서 5줄 -> 15개
    page_size_query_param = 'page_size'


@api_view(['GET'])
def jobs_list(request):
    recruitments = Recruitment.objects.all()

    paginator = JobPagination() # JobPagination 클래스의 인스턴스 생성
    
    page = paginator.paginate_queryset(recruitments, request) # 전체 recruitments 쿼리셋에서 15개만 잘라서 반환
    serializer = RecruitmentListSerializer(page, many=True) # 잘라낸 15개짜리 page를 JSON으로 직렬화
    return paginator.get_paginated_response(serializer.data) # 페이지 정보도 같이 감싸서 반환
    # {
    # "count": 150,
    # "next": "http://.../jobs/?page=2",
    # "previous": null,
    # "results": [ ... ]
    # }

@api_view(['GET'])
def job_detail(request, job_pk):
    recruitment_detail = get_object_or_404(
        RecruitmentDetail.objects.select_related('recruitment__company'),
        recruitment_id=job_pk,
    )
    serializer = RecruitmentDetailReadSerializer(recruitment_detail)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_jobs(request):

    result = fetch_jobs_service()

    return Response(result)


@api_view(['GET'])
def fetch_detail(request):

    result = fetch_detail_service()

    return Response(result)
