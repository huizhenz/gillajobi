import re

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://thinkyou.co.kr" # 기본 도메인
LIST_URL = f"{BASE_URL}/contest/ajax_contestList.asp" # 목록 데이터 받아오는 URL

HEADERS = {
    "Referer": "https://thinkyou.co.kr/contest/", # "나 씽유 사이트에서 온 요청이야" 라고 서버에 알려주는 것
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" # "나 봇 아니고 일반 브라우저야" 라고 속이는 것
}


def crawl_thinkyou(page=1):
    data = {
        "pageSize": "30",
        "page": str(page),
        "serstatus": "",
        "serfield": "",
        "sertarget": "",
        "serprizeMoney": "",
        "serdivision": "",
        "seritem": "",
        "searchstr": ""
    }

    response = requests.post(LIST_URL, headers=HEADERS, data=data)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.tr")

    results = []

    for item in items:
        # 제목
        title_tag = item.select_one("div.title h3")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)

        # 주최
        host_tag = item.select_one("div.title dd")
        host = host_tag.get_text(strip=True).replace("주최 :", "").strip() if host_tag else ""

        # 기간
        etc_tags = item.select("div.etc")
        period = etc_tags[0].get_text(strip=True) if etc_tags else ""

        # 상태
        status_tag = item.select_one("div.statNew p.icon")
        status = status_tag.get_text(strip=True) if status_tag else ""

        # 상세 URL + external_id
        link_tag = item.select_one("div.title a")
        detail_url = ""
        external_id = None
        if link_tag and link_tag.get("href"):
            href = link_tag["href"]
            detail_url = BASE_URL + href if href.startswith("/") else href
            match = re.search(r"/contest/(\d+)/", href)
            external_id = int(match.group(1)) if match else None

        result = {
            "external_id": external_id,
            "title": title,
            "host": host,
            "period": period,
            "status": status,
            "detail_url": detail_url,
        }
        results.append(result)
        print(result)

    print(f"\n총 {len(results)}개 추출 완료")
    return results


if __name__ == "__main__":
    crawl_thinkyou(page=1)