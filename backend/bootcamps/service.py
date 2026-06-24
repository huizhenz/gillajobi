import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime

from bs4 import BeautifulSoup
import requests

from .models import (
    Region,
    Skill,
    Bootcamp,
)

from .serializers import (
    RegionSerializer,
    SkillSerializer,
    BootcampSerializer,
)

BOOTTENT_SITEMAP = "https://boottent.com/camps/sitemap.xml"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# boottent tags → program_process 표시 텍스트
TAG_MAP = {
    "fe": "프론트엔드",
    "be": "백엔드",
    "fullstack": "풀스택",
    "ai": "AI",
    "data": "데이터사이언스",
    "cloud": "클라우드",
    "security": "보안",
    "game": "게임",
    "mobile": "모바일/앱",
    "design": "UX/UI",
    "pm": "기획/PM",
    "devops": "DevOps",
    "embedded": "임베디드",
    "blockchain": "블록체인",
    "etc": "기타",
    "job": "취업준비",
}

# jobOpportunityValues 키 → 채용연계 유형
JOB_OPPORTUNITY_MAP = {
    "ownCompany": "자사 채용연계",
    "partners": "협력사 채용연계",
}



PAGE_SIZE = 20


def fetch_bootcamps_service(page=None):
    from category.models import Label

    # 1. 사이트맵에서 전체 URL 목록 가져오기
    try:
        res = requests.get(BOOTTENT_SITEMAP, headers=HEADERS, timeout=10)
        root = ET.fromstring(res.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        all_urls = [loc.text for loc in root.findall(".//sm:loc", ns)]
    except Exception as e:
        print(f"사이트맵 로드 실패: {e}")
        return {"created": 0, "updated": 0, "total": 0}

    total_pages = (len(all_urls) + PAGE_SIZE - 1) // PAGE_SIZE

    if page is None:
        urls = all_urls
        print(f"전체 {len(all_urls)}개 처리 시작")
    else:
        start = (page - 1) * PAGE_SIZE
        urls = all_urls[start:start + PAGE_SIZE]
        print(f"전체 {len(all_urls)}개 / page={page} ({len(urls)}개 처리)")

    label, _ = Label.objects.get_or_create(name="bootcamp")
    created_count = 0
    updated_count = 0

    # 2. 각 캠프 상세 페이지 순회
    for camp_url in urls:
        try:
            time.sleep(0.3)
            response = requests.get(camp_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")

            # RSC payload를 모두 언이스케이프해서 하나의 문자열로 합치기
            rsc_text = _collect_rsc_text(soup)

            camp_data = _extract_camp_data(soup, rsc_text)

            if not camp_data.get("title"):
                print(f"  title 없음: {camp_url}")
                continue

            # Region
            region = None
            if camp_data.get("region_name"):
                region, _ = Region.objects.get_or_create(
                    name=camp_data["region_name"]
                )

            bootcamp, created = Bootcamp.objects.update_or_create(
                recruitment_url=camp_url,
                defaults={
                    "title": camp_data["title"],
                    "company": camp_data.get("company_name", ""),
                    "category": None,
                    "label": label,
                    "region": region,
                    "program_process": camp_data.get("program_process"),
                    "expense": camp_data.get("expense"),
                    "period": camp_data.get("period"),
                    "participation_time": camp_data.get("participation_time"),
                    "recruitment_linkage": camp_data.get("recruitment_linkage"),
                    "close_date": camp_data.get("close_date"),
                    "close_date_text": camp_data.get("close_date_text"),
                },
            )

            for skill_name in (camp_data.get("skills") or []):
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                bootcamp.skills.add(skill)

            status = "생성" if created else "업데이트"
            print(f"  [{status}] {camp_data['title']}")

            if created:
                created_count += 1
            else:
                updated_count += 1

        except Exception as e:
            print(f"  오류 {camp_url}: {e}")

    result = {
        "created": created_count,
        "updated": updated_count,
        "total": created_count + updated_count,
    }
    if page is not None:
        result["page"] = page
        result["total_pages"] = total_pages
    return result


def _collect_rsc_text(soup):
    """
    Next.js App Router의 self.__next_f.push([1,"..."]) 스크립트를
    언이스케이프하여 하나의 문자열로 합친다.
    raw script 텍스트에서는 \"key\" 로 이스케이프되어 있어
    직접 regex 검색이 불가하므로 반드시 언이스케이프 후 사용.
    """
    parts = []
    for script in soup.find_all("script"):
        raw = (script.string or "").strip()
        if "self.__next_f.push" not in raw:
            continue
        m = re.search(
            r'self\.__next_f\.push\(\[1,"(.+?)"\]\s*\)',
            raw,
            re.DOTALL,
        )
        if not m:
            continue
        inner = m.group(1)
        try:
            parts.append(json.loads('"' + inner + '"'))
        except Exception:
            parts.append(inner.replace('\\"', '"').replace('\\\\', '\\'))
    return "\n".join(parts)


def _parse_camp_object(rsc_text):
    """RSC 텍스트에서 camp JSON 오브젝트를 추출한다 (중괄호 카운팅)."""
    marker = '"camp":{'
    idx = rsc_text.find(marker)
    if idx == -1:
        return None

    brace_start = idx + len('"camp":')
    depth, in_string, escape_next = 0, False, False

    for i in range(brace_start, len(rsc_text)):
        ch = rsc_text[i]
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(rsc_text[brace_start : i + 1])
                except Exception as e:
                    print(f"camp JSON 파싱 실패: {e}")
                    return None
    return None


def _scrape_html_labels(soup):
    """
    ul > li 라벨-값 구조에서 실제 표시되는 텍스트를 추출한다.
    라벨: bg-grey-100 text-grey-600 클래스의 div
    값: 라벨 li의 다음 형제 li
    """
    result = {}
    for label_div in soup.find_all(
        "div",
        class_=lambda c: c and "bg-grey-100" in c and "text-grey-600" in c,
    ):
        label = label_div.get_text(strip=True)
        label_li = label_div.find_parent("li")
        if not label_li:
            continue
        value_li = label_li.find_next_sibling("li")
        if not value_li:
            continue
        result[label] = value_li.get_text(" ", strip=True)
    return result


def _extract_camp_data(soup, rsc_text):
    camp = _parse_camp_object(rsc_text)
    if not camp:
        return {}

    labels = _scrape_html_labels(soup)
    data = {}

    # ── RSC JSON에서 추출 ──────────────────────────────────────

    # 제목
    data["title"] = camp.get("title", "")

    # 회사명: HTML h2[title] 우선 ("회사명 | 강의명" 형식), 없으면 RSC JSON 대체
    company_name = ""
    h2 = soup.find("h2", attrs={"title": lambda t: t and " | " in t})
    if h2:
        company_name = h2["title"].split(" | ")[0].strip()
    if not company_name:
        for c in camp.get("companyIds", []):
            if c.get("companyRole") == "operator":
                company_name = c.get("companyName", "")
                break
    if not company_name:
        company_name = camp.get("company", "")
    data["company_name"] = company_name

    # 수강료 (tuition 숫자 → 만원 단위)
    tuition = camp.get("tuition")
    if tuition is not None:
        data["expense"] = "무료" if tuition == 0 else f"{tuition}만원"

    # 기술 스택 (tracks[].keywords)
    skills = []
    for track in (camp.get("tracks") or []):
        skills.extend(track.get("keywords") or [])
    if skills:
        data["skills"] = list(dict.fromkeys(skills))

    # program_process: RSC tags[0] → TAG_MAP으로 한글 변환
    tags = camp.get("tags") or []
    if tags:
        data["program_process"] = TAG_MAP.get(tags[0], tags[0])

    # recruitment_linkage: jobOpportunityValues 키가 있을 때만 저장
    job_opp = camp.get("jobOpportunityValues") or {}
    if job_opp:
        linkage_parts = [
            JOB_OPPORTUNITY_MAP.get(k, k)
            for k in job_opp
            if k in JOB_OPPORTUNITY_MAP
        ]
        if linkage_parts:
            data["recruitment_linkage"] = ", ".join(linkage_parts)

    # ── HTML 라벨에서 추출 (실제 표시 텍스트) ─────────────────

    # 학습장소 → region_name (첫 단어만: "서울 서울시 ..." → "서울")
    if "학습장소" in labels:
        data["region_name"] = labels["학습장소"].split()[0]
    elif data.get("program_process") in ("온라인", None) and not data.get("region_name"):
        pass  # 온라인 여부를 RSC에서 확인할 수 없으면 그냥 비워둠

    # 수업일정 → period (날짜 범위 부분만 추출)
    if "수업일정" in labels:
        period_raw = labels["수업일정"]
        m = re.match(r"(\d{4}\.\d{2}\.\d{2}\s*~\s*\d{4}\.\d{2}\.\d{2})", period_raw)
        data["period"] = m.group(1) if m else period_raw

    # 요일시간 → participation_time (공백 정규화)
    if "요일시간" in labels:
        data["participation_time"] = " ".join(labels["요일시간"].split())

    # 모집마감 → close_date_text + close_date
    # 포맷1: "2026.06.22 23:59"  포맷2: "2026.06.22 오늘 마감! 모집 중"
    if "모집마감" in labels:
        close_raw = labels["모집마감"]
        m = re.search(r"(\d{4}\.\d{2}\.\d{2})(?:\s+(\d{2}:\d{2}))?", close_raw)
        if m:
            date_part = m.group(1)
            time_part = m.group(2)
            data["close_date_text"] = f"{date_part} {time_part}" if time_part else date_part
            data["close_date"] = _parse_date(date_part)

    return data


def _parse_date(date_str):
    for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str[:10], fmt).date()
        except ValueError:
            continue
    return None


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

