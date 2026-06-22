from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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


@api_view(['GET'])
def bootcamps_list(request):
    bootcamps = Bootcamp.objects.all()
    serializer = BootcampSerializer(bootcamps, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_bootcamps(request):

    result = fetch_bootcamps_service()

    return Response(result)
