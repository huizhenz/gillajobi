import json
import os
import requests
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()

GMS_URL = "https://gms.ssafy.io/gmsapi/api.anthropic.com/v1/messages"


def expand_keywords(query: str) -> list[str]:
    cache_key = f"search_keywords:{query.lower().strip()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    headers = {
        "x-api-key": os.getenv("GMS_KEY"),
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 300,
        "messages": [{
            "role": "user",
            "content": f"""너는 채용/취업 정보 검색 시스템이야.
사용자가 입력한 검색어에서 관련 키워드를 확장해줘.

규칙:
- 직무명, 기술스택, 자격증명의 동의어 포함
- 한글/영문 표현 모두 포함
- 기술명이면 그 기술을 주로 쓰는 직무명도 포함
- 자격증명이면 관련 직무 포함
- 원래 검색어 반드시 포함
- 최대 10개

예시:
- "vite" → ["vite", "프론트엔드", "frontend", "FE", "React", "Vue", "JavaScript", "웹 개발"]
- "SQLD" → ["SQLD", "SQL", "데이터베이스", "DBA", "백엔드", "데이터 엔지니어"]
- "아트" → ["아트", "art", "디자이너", "UI", "UX", "그래픽", "시각디자인"]

검색어: {query}

JSON 배열로만 응답. 다른 텍스트 없이 배열만."""
        }]
    }

    resp = requests.post(GMS_URL, headers=headers, json=body, timeout=10)
    if not resp.ok:
        print(f"[GMS ERROR] status={resp.status_code} body={resp.text}")
        resp.raise_for_status()

    text = resp.json()["content"][0]["text"].strip()

    # 마크다운 코드블록 제거 (```json ... ``` 형태)
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        keywords = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        keywords = [query]

    cache.set(cache_key, keywords, timeout=60 * 60 * 24)
    return keywords
