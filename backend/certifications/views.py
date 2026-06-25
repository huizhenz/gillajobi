from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Certification, Examination
from .serializers import CertificationSerializer, ExaminationSerializer, CertificationDetailSerializer
from .services import get_certification_data, get_examination_data, sync_all_examinations

class CompetitionPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

# Create your views here.
@api_view(['GET'])
def certifications_top3(request):
    top3 = (
        Certification.objects
        .order_by('-view_count')
        .values('id', 'jm_cd', 'name', 'series_name', 'qualification_cl', 'major_job_field', 'category__name', 'view_count')[:3]
    )
    return Response(list(top3))


@api_view(['GET'])
def fetch_certifications(request):
    certifications = Certification.objects.all()
    paginator = CompetitionPagination()

    page = paginator.paginate_queryset(certifications, request) # 전체 recruitments 쿼리셋에서 15개만 잘라서 반환
    serializer = CertificationSerializer(page, many=True) # 잘라낸 15개짜리 page를 JSON으로 직렬화
    return paginator.get_paginated_response(serializer.data) # 페이지 정보도 같이 감싸서 반환

@api_view(['POST'])
def sync_certifications(request):
    try:
        get_certification_data()
        return Response({'message': '동기화 완료'}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({'message': f'동기화 실패: {str(error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def fetch_examinations(request):
    examinations = Examination.objects.all()
    serializer = ExaminationSerializer(examinations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def sync_examinations(request):
    try:
        jm_cd = request.data.get('jm_cd')
        if jm_cd:
            get_examination_data(jm_cd)
        else:
            sync_all_examinations()
        return Response({'message': '동기화 완료'}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({'message': f'동기화 실패: {str(error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def fetch_certification_detail(request, jm_cd):
    certification = Certification.objects.get(jm_cd=jm_cd)
    Certification.objects.filter(jm_cd=jm_cd).update(view_count=F('view_count') + 1)
    serializer = CertificationDetailSerializer(certification)
    return Response(serializer.data, status=status.HTTP_200_OK)