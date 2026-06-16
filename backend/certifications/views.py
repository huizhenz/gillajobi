from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Certification, Examination
from .serializers import CertificationSerializer, ExaminationSerializer
from .services import get_certification_data, get_examination_data, sync_all_examinations

# Create your views here.
@api_view(['GET'])
def fetch_certifications(request):
    certifications = Certification.objects.all()
    serializer = CertificationSerializer(certifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
