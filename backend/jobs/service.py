from bs4 import BeautifulSoup
import requests

from .models import (
    Company,
    Recruitment,
    RecruitmentDetail,
    HiringProcess,
)
from .serializers import (
    CompanySerializer,
    HiringProcessSerializer,
    RecruitmentDetailSerializer,
    RecruitmentListSerializer,
    RecruitmentDetailReadSerializer
)


def get_form_data(page):

    return {
        "currentPageNo": str(page),
        "pageIndex": str(page),
        "resultCnt": "10",
        "sortOrderBy": "DESC",
        "sortField": "DATE",
        "siteClcd": "all",
        "codeDepth1Info": "11000",
        "codeDepth2Info": "11000",
        "benefitSrchAndOr": "O",
        "empTpGbcd": "1",
        "essCertChk": "N",
    }


def fetch_jobs_service():

    url = (
        "https://www.work24.go.kr"
        "/wk/a/b/1200/retriveDtlEmpSrchListInPost.do"
    )

    created_count = 0
    updated_count = 0

    for page in range(1, 11):

        response = requests.post(
            url,
            data=get_form_data(page),
            headers={
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        rows = soup.select('tr[id^="list"]')

        print(
            f"page={page}, rows={len(rows)}"
        )

        for row in rows:

            company_tag = row.select_one(
                "a.cp_name"
            )

            title_tag = row.select_one(
                "a[data-emp-detail]"
            )

            salary_tag = row.select_one(
                "li.dollar"
            )

            member_tags = row.select(
                "li.member span.item.sm"
            )

            work_tags = row.select(
                "li.time span.item.sm"
            )

            region_tag = row.select_one(
                "li.site p"
            )

            date_tags = row.select(
                "p.s1_r"
            )

            salary = (
                " ".join(
                    salary_tag.get_text(
                        " ",
                        strip=True
                    ).split()
                )
                if salary_tag
                else None
            )

            region = (
                " ".join(
                    region_tag.get_text(
                        " ",
                        strip=True
                    ).split()
                )
                if region_tag
                else None
            )

            close_date = None
            created_date = None

            for tag in date_tags:

                text = tag.get_text(
                    strip=True
                )

                if "마감일" in text:

                    close_date = (
                        text.replace(
                            "마감일 :",
                            ""
                        )
                        .replace(
                            "마감일:",
                            ""
                        )
                        .strip()
                    )

                elif "등록일" in text:

                    created_date = (
                        text.replace(
                            "등록일 :",
                            ""
                        )
                        .replace(
                            "등록일:",
                            ""
                        )
                        .strip()
                    )

            company_name = (
                company_tag.get_text(
                    strip=True
                )
                if company_tag
                else None
            )

            recruitment_url = None

            if (
                title_tag
                and title_tag.get("href")
            ):

                recruitment_url = (
                    "https://www.work24.go.kr"
                    + title_tag["href"]
                )

            company, _ = (
                Company.objects.get_or_create(
                    name=company_name
                )
            )

            recruitment, created = (
                Recruitment.objects.update_or_create(
                    recruitment_url=recruitment_url,
                    defaults={
                        "company": company,
                        "title": (
                            title_tag.get_text(
                                strip=True
                            )
                            if title_tag
                            else None
                        ),
                        "career": (
                            member_tags[0].get_text(
                                strip=True
                            )
                            if len(member_tags) > 0
                            else None
                        ),
                        "education": (
                            member_tags[1].get_text(
                                strip=True
                            )
                            if len(member_tags) > 1
                            else None
                        ),
                        "salary": salary,
                        "working_type": (
                            work_tags[0].get_text(
                                strip=True
                            )
                            if len(work_tags) > 0
                            else None
                        ),
                        "employment_type": (
                            work_tags[1].get_text(
                                strip=True
                            )
                            if len(work_tags) > 1
                            else None
                        ),
                        "region": region,
                        "close_date": close_date,
                        "created_date": created_date,
                    }
                )
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

    return {
        "created": created_count,
        "updated": updated_count,
        "total": created_count + updated_count,
    }

def fetch_detail_service():

    recruitments = Recruitment.objects.select_related('company')

    for recruitment in recruitments:

        response = requests.get(
            recruitment.recruitment_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        soup = BeautifulSoup(response.text, "html.parser")

        detail, _ = RecruitmentDetail.objects.get_or_create(
            recruitment=recruitment
        )

        # =====================
        # 직무내용
        # =====================

        job_title = soup.find("strong", string="직무내용")

        if job_title:
            job_box = job_title.parent

            detail.job_description = (
                job_box.get_text("\n", strip=True)
                .replace("직무내용", "")
                .strip()
            )

        # =====================
        # 상세 테이블 정보
        # =====================

        for row in soup.select("table.box_table tr"):

            ths = row.select("th")
            tds = row.select("td")

            for th, td in zip(ths, tds):

                title = th.get_text(" ", strip=True)

                clean_title = (
                    title
                    .replace(" ", "")
                    .replace("\n", "")
                    .replace("\t", "")
                )

                value = td.get_text(" ", strip=True)
                value = " ".join(value.split())

                # Recruitment

                if "모집인원" in clean_title:
                    try:
                        recruitment.recruitment_count = int(
                            value.replace("명", "")
                        )
                    except:
                        pass

                elif clean_title == "경력":
                    recruitment.career = value

                elif clean_title == "학력":
                    recruitment.education = value

                elif "고용형태" in clean_title:
                    recruitment.employment_type = value

                elif "임금조건" in clean_title:
                    recruitment.salary = value

                elif "근무형태" in clean_title:
                    recruitment.working_type = value

                elif "근무예정지" in clean_title:
                    recruitment.region = value
                    detail.address = value

                elif "구인인증번호" in clean_title:
                    recruitment.wanted_auth_no = value

                # RecruitmentDetail

                elif "자격면허" in clean_title:
                    detail.license = value

                elif clean_title == "전공":
                    detail.qualification = value

                elif "컴퓨터활용능력" in clean_title:
                    detail.computer_skill = value

                elif "외국어능력" in clean_title:
                    detail.foreign_language = value

                elif "기타우대사항" in clean_title:
                    detail.preferred_qualification = value

                elif "근무시간" in clean_title:
                    detail.working_hours = value

                elif "휴게시간" in clean_title:
                    detail.break_time = value

                elif "사회보험" in clean_title:
                    detail.social_insurance = value

                elif "퇴직급여" in clean_title:
                    detail.retirement_pay = value

                elif "접수방법" in clean_title:
                    detail.application_method = value

                elif "제출서류" in clean_title:
                    detail.submission_documents = value

        recruitment.save()
        detail.save()

        # =====================
        # 전형방법
        # =====================

        HiringProcess.objects.filter(
            recruitment=recruitment
        ).delete()

        for process in soup.select(
            "ul.emp_box_items.line li:not(.disable)"
        ):

            process_name = process.get_text(" ", strip=True)

            if process_name:
                HiringProcess.objects.create(
                    recruitment=recruitment,
                    name=process_name
                )

    return {
        "message": "detail saved"
    }