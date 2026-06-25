from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import (
    Region,
    Skill,
    Bootcamp
)
from category.models import Category
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

    region = request.GET.get('region', '').strip()
    category = request.GET.get('category', '').strip()
    if region:
        bootcamps = bootcamps.filter(region__name__icontains=region)
    if category:
        bootcamps = bootcamps.filter(category__name__icontains=category)
    if region or category:
        bootcamps = bootcamps.distinct()

    paginator = BootcampPagination()
    page = paginator.paginate_queryset(bootcamps, request)
    serializer = BootcampSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def regions_list(request):
    regions = Region.objects.values_list('name', flat=True).order_by('name')
    return Response(list(regions))


@api_view(['GET'])
def categories_list(request):
    categories = (
        Category.objects
        .filter(bootcamps__isnull=False)
        .values_list('name', flat=True)
        .distinct()
        .order_by('name')
    )
    return Response(list(categories))

@api_view(['GET'])
def bootcamp_detail(request, bootcamp_pk):
    bootcamp = get_object_or_404(Bootcamp, pk=bootcamp_pk)
    Bootcamp.objects.filter(pk=bootcamp_pk).update(view_count=F('view_count') + 1)
    serializer = BootcampSerializer(bootcamp)
    return Response(serializer.data)



@api_view(['GET'])
def bootcamps_top3(request):
    top3 = (
        Bootcamp.objects
        .order_by('-view_count')
        .values('id', 'title', 'company', 'view_count')[:3]
    )
    return Response(list(top3))


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
