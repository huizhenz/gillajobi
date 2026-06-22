from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Competition
from .serializers import CompetitionSerializer
from .services import run_sync

# Create your views here.
@api_view(['GET'])
def fetch_competitions(request):
    competitions = Competition.objects.all()
    serializer = CompetitionSerializer(competitions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def sync_competitions(request):
    total_saved = run_sync()
    return Response({"saved": total_saved}, status=status.HTTP_200_OK)


@api_view(['GET'])
def fetch_competition_detail(request, pk):
    competitions = Competition.objects.get(pk=pk)
    serializer = CompetitionSerializer(competitions)
    return Response(serializer.data, status=status.HTTP_200_OK)
