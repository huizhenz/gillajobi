from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Competition
from .serializers import CompetitionSerializer
from .services import sync_competitions

# Create your views here.
@api_view(['GET'])
def fetch_competitions(request):
    sync_competitions()
    competitions = Competition.objects.all()
    serializer = CompetitionSerializer(competitions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# def sync_competitions(request):
#     pass
