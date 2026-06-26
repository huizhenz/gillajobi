from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import (
    Recruitment,
    RecruitmentDetail,
)
from .serializers import (
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

    region = request.GET.get('region', '').strip()
    if region:
        recruitments = recruitments.filter(region__startswith=region)

    paginator = JobPagination()
    page = paginator.paginate_queryset(recruitments, request)
    serializer = RecruitmentListSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def regions_list(request):
    all_regions = (
        Recruitment.objects
        .exclude(region__isnull=True)
        .exclude(region='')
        .values_list('region', flat=True)
    )
    short_regions = sorted(set(r[:2] for r in all_regions if r))
    return Response(short_regions)

@api_view(['GET'])
def job_detail(request, job_pk):
    recruitment_detail = get_object_or_404(
        RecruitmentDetail.objects.select_related('recruitment__company'),
        recruitment_id=job_pk,
    )
    Recruitment.objects.filter(pk=job_pk).update(
        view_count=Coalesce(F('view_count'), 0) + 1
    )
    serializer = RecruitmentDetailReadSerializer(recruitment_detail)
    return Response(serializer.data)


@api_view(['GET'])
def jobs_top3(request):
    top3 = (
        Recruitment.objects
        .order_by('-view_count')
        .values('id', 'title', 'company__name', 'category__name', 'view_count')[:3]
    )
    return Response(list(top3))


@api_view(['GET'])
def fetch_jobs(request):

    result = fetch_jobs_service()

    return Response(result)


@api_view(['GET'])
def fetch_detail(request):

    result = fetch_detail_service()

    return Response(result)
