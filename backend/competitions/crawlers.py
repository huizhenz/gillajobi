import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://thinkyou.co.kr"
LIST_URL = f"{BASE_URL}/contest/ajax_contestList.asp"

HEADERS = {
    "Referer": "https://thinkyou.co.kr/contest/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

ACTIVE_STATUSES = {"접수중", "접수예정", "마감임박"}


def parse_period(period_str):
    """'26-06-17 ~ 26-08-26' → (date, date)"""
    try:
        parts = period_str.split("~")
        start = datetime.strptime(parts[0].strip(), "%y-%m-%d").date()
        end = datetime.strptime(parts[1].strip(), "%y-%m-%d").date()
        return start, end
    except Exception:
        return None, None


STATUS_KEYWORDS = ["마감임박", "접수중", "접수예정", "마감"]

def parse_status(raw):
    """'접수중D-69' → '접수중'"""
    for s in STATUS_KEYWORDS:
        if raw.startswith(s):
            return s
    return raw


def crawl_page(page):
    data = {
        "pageSize": "40",
        "page": str(page),
        "serstatus": "",
        "serfield": "",
        "sertarget": "",
        "serprizeMoney": "",
        "serdivision": "",
        "seritem": "",
        "searchstr": ""
    }

    try:
        response = requests.post(LIST_URL, headers=HEADERS, data=data, timeout=10)
        response.encoding = "utf-8"
    except requests.exceptions.Timeout:
        print(f"[page {page}] 요청 타임아웃. 건너뜀.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[page {page}] 네트워크 오류: {e}. 건너뜀.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.tr")
    results = []

    for item in items:
        try:
            title_tag = item.select_one("div.title h3")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            host_tag = item.select_one("div.title dd")
            host = host_tag.get_text(strip=True).replace("주최 :", "").strip() if host_tag else ""

            etc_tags = item.select("div.etc")
            period_raw = etc_tags[0].get_text(strip=True) if etc_tags else ""
            start_date, end_date = parse_period(period_raw)

            status_tag = item.select_one("div.statNew p.icon")
            status_raw = status_tag.get_text(strip=True) if status_tag else ""
            status = parse_status(status_raw)

            link_tag = item.select_one("div.title a")
            detail_url = ""
            external_id = None
            if link_tag and link_tag.get("href"):
                href = link_tag["href"]
                detail_url = BASE_URL + href if href.startswith("/") else href
                match = re.search(r"/contest/(\d+)/", href)
                external_id = int(match.group(1)) if match else None

            results.append({
                "external_id": external_id,
                "title": title,
                "host": host,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "detail_url": detail_url,
            })

        except Exception as e:
            print(f"[page {page}] 항목 파싱 오류: {e}. 건너뜀.")
            continue

    return results


def crawl_all():
    page = 1
    all_results = []

    while True:
        print(f"[page {page}] 크롤링 중...")
        results = crawl_page(page)

        if not results:
            print("결과 없음. 종료.")
            break

        active = [r for r in results if r["status"] in ACTIVE_STATUSES]
        if not active:
            print(f"[page {page}] 활성 공모전 없음. 종료.")
            break

        all_results.extend(active)
        page += 1
        time.sleep(0.5)

    return all_results
