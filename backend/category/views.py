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

    jobs = list(Recruitment.objects.filter(make_filter([
        'title', 'company__name', 'detail__job_description', 'detail__qualification'
    ])).distinct().values('id', 'title', 'company__name', 'close_date')[:(limit_label if label == 'jobs' else limit_all)]) if should_query('jobs') else []

    bootcamps = list(Bootcamp.objects.filter(make_filter([
        'title', 'program_process', 'skills__name'
    ])).distinct().values('id', 'title', 'company', 'close_date')[:(limit_label if label == 'bootcamps' else limit_all)]) if should_query('bootcamps') else []

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
