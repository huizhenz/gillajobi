import time
from datetime import datetime

from bs4 import BeautifulSoup
import requests

from .models import (
    Company,
    Recruitment,
    RecruitmentDetail,
    HiringProcess,
)

BASE_URL = "https://www.work24.go.kr"
LIST_URL = BASE_URL + "/wk/a/b/1200/retriveDtlEmpSrchListInPost.do"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def _get_form_data(page):
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


def _parse_date(text):
    for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text.strip()[:10], fmt).date()
        except ValueError:
            continue
    return None


def _parse_list_row(row):
    company_tag = row.select_one("a.cp_name")
    title_tag = row.select_one("a[data-emp-detail]")
    salary_tag = row.select_one("li.dollar")
    member_tags = row.select("li.member span.item.sm")
    work_tags = row.select("li.time span.item.sm")
    region_tag = row.select_one("li.site p")
    date_tags = row.select("p.s1_r")

    if not title_tag:
        return None

    href = title_tag.get("href")
    recruitment_url = (BASE_URL + href) if href else None
    if not recruitment_url:
        return None

    company_name = company_tag.get_text(strip=True) if company_tag else None
    if not company_name:
        return None

    salary = (
        " ".join(salary_tag.get_text(" ", strip=True).split())
        if salary_tag else None
    )
    region = (
        " ".join(region_tag.get_text(" ", strip=True).split())
        if region_tag else None
    )

    close_date = None
    created_date = None
    for tag in date_tags:
        text = tag.get_text(strip=True)
        if "마감일" in text:
            raw = text.replace("마감일 :", "").replace("마감일:", "").strip()
            close_date = _parse_date(raw)
        elif "등록일" in text:
            raw = text.replace("등록일 :", "").replace("등록일:", "").strip()
            created_date = _parse_date(raw)

    return {
        "company_name": company_name,
        "recruitment_url": recruitment_url,
        "title": title_tag.get_text(strip=True),
        "career": member_tags[0].get_text(strip=True) if len(member_tags) > 0 else None,
        "education": member_tags[1].get_text(strip=True) if len(member_tags) > 1 else None,
        "salary": salary,
        "working_type": work_tags[0].get_text(strip=True) if len(work_tags) > 0 else None,
        "employment_type": work_tags[1].get_text(strip=True) if len(work_tags) > 1 else None,
        "region": region,
        "close_date": close_date,
        "created_date": created_date,
    }


def fetch_jobs_service():
    created_count = 0
    updated_count = 0

    for page in range(1, 11):
        try:
            time.sleep(0.3)
            response = requests.post(
                LIST_URL,
                data=_get_form_data(page),
                headers=HEADERS,
                timeout=15,
            )
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.select('tr[id^="list"]')
            print(f"page={page}, rows={len(rows)}")
        except Exception as e:
            print(f"page={page} 요청 실패: {e}")
            continue

        for row in rows:
            try:
                data = _parse_list_row(row)
                if not data:
                    continue

                company, _ = Company.objects.get_or_create(name=data["company_name"])

                _, created = Recruitment.objects.update_or_create(
                    recruitment_url=data["recruitment_url"],
                    defaults={
                        "company": company,
                        "title": data["title"],
                        "career": data["career"],
                        "education": data["education"],
                        "salary": data["salary"],
                        "working_type": data["working_type"],
                        "employment_type": data["employment_type"],
                        "region": data["region"],
                        "close_date": data["close_date"],
                        "created_date": data["created_date"],
                    },
                )

                status = "생성" if created else "업데이트"
                print(f"  [{status}] {data['title']}")

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                print(f"  행 처리 오류: {e}")

    return {
        "created": created_count,
        "updated": updated_count,
        "total": created_count + updated_count,
    }


def fetch_detail_service():
    recruitments = Recruitment.objects.select_related("company")

    for recruitment in recruitments:
        try:
            time.sleep(0.3)
            response = requests.get(
                recruitment.recruitment_url,
                headers=HEADERS,
                timeout=15,
            )
            soup = BeautifulSoup(response.text, "html.parser")

            detail, _ = RecruitmentDetail.objects.get_or_create(recruitment=recruitment)

            # 직무내용
            job_title = soup.find("strong", string="직무내용")
            if job_title:
                job_box = job_title.parent
                detail.job_description = (
                    job_box.get_text("\n", strip=True)
                    .replace("직무내용", "")
                    .strip()
                )

            # 상세 테이블
            for row in soup.select("table.box_table tr"):
                ths = row.select("th")
                tds = row.select("td")

                for th, td in zip(ths, tds):
                    clean_title = (
                        th.get_text(" ", strip=True)
                        .replace(" ", "")
                        .replace("\n", "")
                        .replace("\t", "")
                    )
                    value = " ".join(td.get_text(" ", strip=True).split())

                    if "모집인원" in clean_title:
                        try:
                            recruitment.recruitment_count = int(value.replace("명", ""))
                        except ValueError:
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

            # 전형방법
            HiringProcess.objects.filter(recruitment=recruitment).delete()
            for process in soup.select("ul.emp_box_items.line li:not(.disable)"):
                process_name = process.get_text(" ", strip=True)
                if process_name:
                    HiringProcess.objects.create(
                        recruitment=recruitment,
                        name=process_name,
                    )

            print(f"  [상세] {recruitment.title}")

        except Exception as e:
            print(f"  오류 {recruitment.recruitment_url}: {e}")

    return {"message": "detail saved"}
