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
