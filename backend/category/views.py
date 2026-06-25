import os
import requests as http_requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .services import expand_keywords
from jobs.models import Recruitment
from bootcamps.models import Bootcamp
from certifications.models import Certification
from competitions.models import Competition


@api_view(['GET'])
def search(request):
    q = request.GET.get('q', '').strip()
    label = request.GET.get('label', None)  # jobs | bootcamps | certifications | competitions
    if not q:
        return Response({"jobs": [], "bootcamps": [], "certifications": [], "competitions": []})

    keywords = expand_keywords(q)

    def make_filter(fields):
        q_filter = Q()
        for kw in keywords:
            for field in fields:
                q_filter |= Q(**{f"{field}__icontains": kw})
        return q_filter


    limit_all = 5
    limit_label = 50

    def should_query(name):
        return label is None or label == name

    region = request.GET.get('region', '').strip()
    bc_category = request.GET.get('category', '').strip()

    jobs_qs = Recruitment.objects.filter(make_filter([
        'title', 'company__name', 'detail__job_description', 'detail__qualification'
    ])).distinct()
    if region:
        jobs_qs = jobs_qs.filter(region__startswith=region)
    jobs = list(jobs_qs.values('id', 'title', 'company__name', 'close_date')[:(limit_label if label == 'jobs' else limit_all)]) if should_query('jobs') else []

    bootcamps_qs = Bootcamp.objects.filter(make_filter([
        'title', 'program_process', 'skills__name'
    ])).distinct()
    if region:
        bootcamps_qs = bootcamps_qs.filter(region__name__icontains=region)
    if bc_category:
        bootcamps_qs = bootcamps_qs.filter(category__name__icontains=bc_category)
    if region or bc_category:
        bootcamps_qs = bootcamps_qs.distinct()
    bootcamps = list(bootcamps_qs.values('id', 'title', 'company', 'close_date')[:(limit_label if label == 'bootcamps' else limit_all)]) if should_query('bootcamps') else []

    certifications = list(Certification.objects.filter(make_filter([
        'name', 'major_job_field', 'minor_job_field'
    ])).distinct().values('id', 'jm_cd', 'name', 'series_name')[:(limit_label if label == 'certifications' else limit_all)]) if should_query('certifications') else []

    competitions = list(Competition.objects.filter(make_filter([
        'title', 'keyword'
    ])).distinct().values('id', 'title', 'host', 'keyword', 'start_date')[:(limit_label if label == 'competitions' else limit_all)]) if should_query('competitions') else []

    return Response({
        "jobs": jobs,
        "bootcamps": bootcamps,
        "certifications": certifications,
        "competitions": competitions,
    })


@api_view(['GET'])
def news(request):
    api_key = os.getenv('NEWS_API_KEY')
    try:
        resp = http_requests.get(
            'https://api.kcisa.kr/openapi/service/rest/meta14/getKCPG051802',
            params={'serviceKey': api_key, 'numOfRows': 12, 'pageNo': 1},
            headers={'Accept': 'application/json'},
            timeout=8,
        )
        data = resp.json()
        body = data.get('response', {}).get('body', {})
        items = body.get('items', [])
        if isinstance(items, dict):
            items = items.get('item', [])
        if isinstance(items, dict):
            items = [items]
        result = [
            {
                'title': item.get('title', ''),
                'thumbnail': item.get('referenceIdentifier', ''),
                'url': item.get('url') or item.get('identifier', ''),
            }
            for item in (items or [])
            if item.get('title')
        ]
        return Response({'news': result})
    except Exception:
        return Response({'news': []})
