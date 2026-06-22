from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

from django.conf import settings

@api_view(['GET'])
def jobs_list(request):
    recruitments = Recruitment.objects.all()
    serializer = RecruitmentListSerializer(recruitments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def job_detail(request, job_pk):
    recruitment = Recruitment.objects.get(pk=job_pk)
    serializer = RecruitmentDetailReadSerializer(recruitment)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_jobs(request):

    result = fetch_jobs_service()

    return Response(result)

@api_view(['GET'])
def fetch_detail(request):

    result = fetch_detail_service()

    return Response(result)
