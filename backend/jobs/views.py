from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Recruitment, Company
from .serializers import RecruitmentSerializer, CompanySerializer

from bs4 import BeautifulSoup
import requests
from django.conf import settings

@api_view(['GET'])
def jobs_list(request):
    recruitments = Recruitment.objects.all()
    serializer = RecruitmentSerializer(recruitments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def job_detail(request, job_pk):
    recruitment = Recruitment.objects.get(pk=job_pk)
    serializer = RecruitmentSerializer(recruitment)
    return Response(serializer.data)


# @api_view(['GET'])
# def fetch_jobs(request):

#     url = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L01.do"

#     params = {
#         "serviceKey": "발급받은_인증키",
#     }

#     response = request.get(url, params=params)

#     if response.status_code != 200:
#         return Response(
#             {"error": "API 호출 실패"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     data = response.json()

#     jobs = data['jobs']

#     for job in jobs:

#         company, _ = Company.objects.get_or_create(
#             name=job['companyNm']
#         )

#         Recruitment.objects.create(
#             company=company,
#             title=job['wantedTitle']
#         )

#     return Response(
#         {"message": "저장 완료"},
#         status=status.HTTP_201_CREATED
#     )

# @api_view(['GET'])
# def fetch_jobs(request):

#     url = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo215L11.do"

#     params = {
#         "authKey": settings.WORK24_API_KEY,
#         "returnType": "XML",
#     }

#     response = requests.get(url, params=params)

#     return Response({
#         "status_code": response.status_code,
#         "response": response.text[:5000]
#     })

@api_view(['GET'])
def fetch_jobs(request):

    url = "https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    rows = soup.select('tr[id^="list"]')

    for row in rows:

        company_tag = row.select_one("a.cp_name")
        title_tag = row.select_one("a[data-emp-detail]")

        salary_tag = row.select_one("li.dollar")
        member_tags = row.select("li.member span.item.sm")

        work_tags = row.select("li.time span.item.sm")

        region_tag = row.select_one("li.site p")

        close_date_tag = row.select_one("p.s1_r")

        salary = (
            " ".join(
                salary_tag.get_text(separator=" ", strip=True).split()
            )
            if salary_tag
            else None
        )

        region = (
            " ".join(
                region_tag.get_text(separator=" ", strip=True).split()
            )
            if region_tag
            else None
        )

        jobs.append({
            "company": (
                company_tag.get_text(strip=True)
                if company_tag
                else None
            ),

            "title": (
                title_tag.get_text(strip=True)
                if title_tag
                else None
            ),

            "salary": salary,

            "career": (
                member_tags[0].get_text(strip=True)
                if len(member_tags) > 0
                else None
            ),

            "education": (
                member_tags[1].get_text(strip=True)
                if len(member_tags) > 1
                else None
            ),

            "working_days": (
                work_tags[0].get_text(strip=True)
                if len(work_tags) > 0
                else None
            ),

            "working_hours": (
                work_tags[1].get_text(strip=True)
                if len(work_tags) > 1
                else None
            ),

            "region": region,

            "close_date": (
                close_date_tag.get_text(strip=True)
                .replace("마감일 :", "")
                .replace("마감일:", "")
                if close_date_tag
                else None
            ),

            "recruitment_url": (
                "https://www.work24.go.kr"
                + title_tag["href"]
                if title_tag
                else None
            ),
        })

    return Response(jobs)