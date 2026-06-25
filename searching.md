# 검색 기능 설계 문서

## 개요

채용공고·부트캠프·자격증·공모전 데이터(SQLite)에 대해 사용자가 자연어로 검색할 수 있는 시스템.  
단순 문자열 매칭을 넘어 **의미 기반 키워드 확장**을 통해 검색 품질을 높인다.

---

## 핵심 문제

| 사용자 입력 | DB에 저장된 표현 | icontains 단독 |
|------------|----------------|---------------|
| "아트" | "디자이너", "UI/UX" | ❌ 미탐지 |
| "vite" | "프론트엔드 개발자" | ❌ 미탐지 |
| "회계" | "경리", "Finance" | ❌ 미탐지 |
| "SQLD" | "데이터베이스 관련 직무" | ❌ 미탐지 |

→ 검색어와 DB 데이터의 **표현 불일치** 문제를 해결해야 한다.

---

## 아키텍처

```
[사용자 입력]
      │
      ▼ 검색어 입력 후 엔터
[Vue 3 프론트 — MainView]
      │ router.push('/search')
      ▼
[SearchView — onMounted]
      │ searchStore.search() 호출
      ▼ GET /api/v1/category/search/?q=검색어
[DRF View — category/views.py]
      │
      ├─ 캐시 HIT ──────────────────────────────────────┐
      │                                                  │
      ▼ 캐시 MISS                                        │
[Claude Haiku API] 키워드 확장                           │
  "vite" → ["vite", "프론트엔드", "frontend",           │
             "React", "Vue", "JavaScript", "FE"]        │
      │                                                  │
      ▼ 캐시 저장 (24시간)                               │
[SQLite icontains OR 검색] ◀────────────────────────────┘
  대상: jobs / bootcamps / certifications / competitions
      │
      ▼
[JSON 응답 — 4개 카테고리]
```

---

## 사용 기술 및 모델

### AI 모델: Claude Haiku 4.5

| 항목 | 내용 |
|------|------|
| 모델명 | `claude-haiku-4-5-20251001` |
| 역할 | 검색어 → 관련 키워드 배열 확장 |
| 평균 응답시간 | ~0.8~1초 |
| 선택 이유 | 키워드 확장은 단순 작업이므로 Haiku로 충분, Sonnet 대비 2~3배 빠름 |
| 컨텍스트 창(Context window) | 200,000 tokens |
| 최대 출력(Max output) | 64,000 tokens |
| max_tokens (앱 설정값) | 300 (JSON 배열만 반환하므로 충분; 모델 최대치 대비 극히 일부만 사용) |

### 백엔드: Django REST Framework

- `icontains` OR 필터로 다중 키워드 동시 검색
- Django 내장 캐시 프레임워크(LocMemCache)로 API 호출 결과 저장
- 검색 대상 모델 및 필드:

| 모델 | 검색 필드 |
|------|-----------|
| `Recruitment` (채용공고) | `title`, `company__name`, `detail__job_description`, `detail__qualification` |
| `Bootcamp` (부트캠프) | `title`, `program_process`, `skills__name` |
| `Certification` (자격증) | `name`, `major_job_field`, `minor_job_field` |
| `Competition` (공모전) | `title`, `keyword` |

### 프론트엔드: Vue 3 + Pinia

- `searchStore.keyword`에 검색어 바인딩
- 검색 후 `/search` 라우트 이동 → `SearchView.onMounted`에서 `searchStore.search()` 1회 호출
- 결과: `results.jobs`, `results.bootcamps`, `results.certifications`, `results.competitions`

---

## 상세 구현

### 1. Django 캐시 설정 (`settings.py`)

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
```

### 2. 키워드 확장 서비스 (`category/services.py`)

```python
import json
from anthropic import Anthropic
from django.core.cache import cache

def expand_keywords(query: str) -> list[str]:
    cache_key = f"search_keywords:{query.lower().strip()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    client = Anthropic()  # ANTHROPIC_API_KEY 환경변수
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"""
너는 채용/취업 정보 검색 시스템이야.
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

JSON 배열로만 응답. 다른 텍스트 없이 배열만.
"""
        }]
    )

    keywords = json.loads(response.content[0].text)
    cache.set(cache_key, keywords, timeout=60 * 60 * 24)
    return keywords
```

### 3. 검색 뷰 (`category/views.py`)

```python
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
    if not q:
        return Response({"jobs": [], "bootcamps": [], "certifications": [], "competitions": []})

    keywords = expand_keywords(q)

    def make_filter(fields):
        q_filter = Q()
        for kw in keywords:
            for field in fields:
                q_filter |= Q(**{f"{field}__icontains": kw})
        return q_filter

    jobs = list(Recruitment.objects.filter(make_filter([
        'title', 'company__name', 'detail__job_description', 'detail__qualification'
    ])).distinct().values('id', 'title', 'company__name')[:5])

    bootcamps = list(Bootcamp.objects.filter(make_filter([
        'title', 'program_process', 'skills__name'
    ])).distinct().values('id', 'title')[:5])

    certifications = list(Certification.objects.filter(make_filter([
        'name', 'major_job_field', 'minor_job_field'
    ])).distinct().values('id', 'name')[:5])

    competitions = list(Competition.objects.filter(make_filter([
        'title', 'keyword'
    ])).distinct().values('id', 'title')[:5])

    return Response({
        "jobs": jobs,
        "bootcamps": bootcamps,
        "certifications": certifications,
        "competitions": competitions,
    })
```

### 4. URL 등록 (`category/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'category'
urlpatterns = [
    path('search/', views.search),
]
```

### 5. 프론트엔드 검색 스토어 (`stores/searchStore.js`)

```javascript
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  const keyword = ref('')
  const results = ref({
    jobs: [],
    bootcamps: [],
    certifications: [],
    competitions: [],
  })

  const search = function () {
    if (!keyword.value.trim()) return
    axios.get('http://127.0.0.1:8000/api/v1/category/search/', {
      params: { q: keyword.value }
    })
    .then(res => results.value = res.data)
    .catch(err => console.log(err))
  }

  return { keyword, results, search }
})
```

---

## 예상 응답 시간

```
Claude Haiku API       ~800ms (캐시 MISS 시)
SQLite OR 검색         ~50ms
------------------------------------------
최초 검색 (캐시 MISS)  ~850ms
재검색   (캐시 HIT)    ~50ms 이하
```

캐시 HIT 시 Claude API 호출이 없으므로 거의 즉시 응답.

---

## 확장 고려사항

### 검색 품질 개선이 필요할 때
- few-shot 예시를 프롬프트에 추가해 도메인 특화 키워드 확장 강화
- 자주 쓰이는 검색어 top 50을 미리 워밍업(pre-cache)

### 데이터 규모가 커질 때 (10만건+)
- SQLite FTS5 가상 테이블로 전환
- 벡터 임베딩 기반 시맨틱 서치 도입 검토

### 비용 절감이 필요할 때
- 캐시 TTL 연장 (24시간 → 7일)
- 검색어 정규화 (소문자 변환, 공백 제거) 후 캐시 키 통일