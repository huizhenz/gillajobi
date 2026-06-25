# 길라잡이 (Gillajobi)

취업 준비생을 위한 채용 정보 통합 플랫폼. 채용공고, 부트캠프, 자격증, 공모전 정보를 한 곳에서 제공하며, AI 기반 자연어 검색을 지원한다.

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | Django 5.2, Django REST Framework, dj-rest-auth, django-allauth |
| Frontend | Vue 3, Pinia, Vue Router, Axios, SCSS, Pretendard 폰트(npm) |
| DB | SQLite |
| 인증 | Token Authentication |
| 데이터 수집 | Requests, BeautifulSoup4 (크롤링) |
| AI | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) — 검색어 키워드 확장 (Context window: 200,000 tokens / Max output: 64,000 tokens) |

---

## 프로젝트 구조

```
gillajobi/
├── backend/                  # Django REST API 서버
│   ├── gillajobi/            # 프로젝트 설정 (settings.py, urls.py)
│   ├── accounts/             # 회원가입 / 로그인 / 프로필
│   ├── bootcamps/            # 부트캠프 정보
│   ├── certifications/       # 국가자격증 & 시험 일정
│   ├── competitions/         # 공모전 / 해커톤
│   ├── community/            # 커뮤니티 게시글 & 댓글
│   ├── jobs/                 # 채용공고
│   ├── todos/                # 사용자 할일 관리
│   ├── category/             # 공통 카테고리 & 검색 (AI 키워드 확장)
│   └── ai_score/             # AI 적합도 점수 (개발 예정)
│
├── fixtures/                 # 통합 픽스처 (total.json)
│
└── frontend/                 # Vue.js 클라이언트
    └── src/
        ├── views/            # 페이지 컴포넌트
        ├── components/       # 재사용 UI 컴포넌트
        │   └── common/       # SearchBox, AppNav, AppFooter
        ├── stores/           # Pinia 상태 관리
        └── router/           # Vue Router 설정
```

---

## 실행 방법

### Backend
```bash
cd backend
pip install -r requirements.txt
pip install anthropic          # AI 검색 의존성
python manage.py migrate
python manage.py runserver     # http://127.0.0.1:8000
```

> `backend/.env`에 `GMS_KEY`가 설정되어 있어야 AI 검색이 동작합니다.

### Frontend
```bash
cd frontend
npm install
npm run dev                    # http://localhost:5173
```

---

## API 엔드포인트

Base URL: `http://127.0.0.1:8000/api/v1`

### Accounts
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/accounts/registration/` | 회원가입 |
| POST | `/accounts/login/` | 로그인 (토큰 발급) |
| POST | `/accounts/logout/` | 로그아웃 |
| GET / PATCH | `/accounts/profile/` | 프로필 조회 / 수정 |

### Bootcamps
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/bootcamps/` | 부트캠프 목록 (`?region=`, `?category=` 필터 지원) |
| GET | `/bootcamps/<bootcamp_pk>/` | 부트캠프 상세 |
| GET | `/bootcamps/regions/` | 지역 목록 (드롭다운용) |
| GET | `/bootcamps/categories/` | 카테고리 목록 (드롭다운용, 연결된 bootcamp 있는 것만) |
| GET | `/bootcamps/fetch/` | 외부 사이트(boottent.com) 크롤링 후 저장 (`?page=N` 옵션) |

### Jobs
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/jobs/` | 채용공고 목록 (`?region=` 필터 지원, 앞 2글자 prefix 매칭) |
| GET | `/jobs/<job_pk>/` | 채용공고 상세 |
| GET | `/jobs/regions/` | 지역 목록 (앞 2글자로 축약·중복 제거, 드롭다운용) |
| GET | `/jobs/fetch/` | work24.go.kr 크롤링 후 저장 |
| GET | `/jobs/fetch_detail/` | 채용공고 상세 정보 크롤링 |

### Certifications
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/certifications/fetch/` | 자격증 목록 |
| POST | `/certifications/sync/` | 한국산업인력공단 API 동기화 |
| GET | `/certifications/fetch/exam/` | 시험 일정 목록 |
| POST | `/certifications/sync/exam/` | 시험 일정 동기화 (`?jm_cd=` 옵션) |
| GET | `/certifications/fetch/detail/<jm_cd>/` | 자격증 상세 (시험 일정 포함) |

### Competitions
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/competitions/fetch/` | 공모전 목록 |
| POST | `/competitions/sync/` | 외부 크롤링 후 DB 동기화 |
| GET | `/competitions/fetch/detail/<pk>/` | 공모전 상세 |

### Community
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/community/labels/` | 카테고리(레이블) 목록 |
| GET / POST | `/community/articles/` | 게시글 목록 / 작성 |
| GET / PUT / DELETE | `/community/articles/<id>/` | 게시글 상세 / 수정 / 삭제 |
| GET / POST | `/community/articles/<id>/comments/` | 댓글 목록 / 작성 |
| DELETE | `/community/comments/<id>/` | 댓글 삭제 |

### Search (AI 키워드 확장)
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/category/search/?q=검색어` | 자연어 검색 — Claude AI로 키워드 확장 후 4개 카테고리 동시 검색. `label` 미지정: 각 5건 / `label` 지정: 해당 카테고리만 50건. `region`(jobs·bootcamps), `category`(bootcamps) 필터 조합 가능 |

### Todos
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET / POST | `/todos/` | 할일 목록 / 생성 |
| PUT / DELETE | `/todos/<id>/` | 할일 수정 / 삭제 |

---

## AI 검색 구조

```
[사용자 입력]
      │
      ▼
[SearchBox.vue] — label prop으로 동작 분기
      │
      ├─ label=null (MainView): router.push('/search') → input 초기화
      │       ▼
      │  [SearchView — onMounted → searchStore.search()]
      │       │ GET /api/v1/category/search/?q=검색어
      │       ▼
      │  [JSON 응답] → .slice(0, 3) → 4개 섹션 각 최대 3건 표시
      │
      └─ label='jobs'|'bootcamps'|'certifications'|'competitions'
              │ GET /api/v1/category/search/?q=검색어&label=jobs[&region=서울][&category=IT]
              ▼
         [해당 카테고리만 최대 50건] → List 컴포넌트 인라인 표시 후 input 초기화
              ▼
         [0건이면 "키워드에 일치하는 정보가 없습니다." 출력]

공통 흐름:
      GET /api/v1/category/search/
              │
              ├─ 캐시 HIT (LocMemCache, 24시간) ──────────────┐
              │                                                │
              ▼ 캐시 MISS                                      │
      [category/services.py — expand_keywords()]              │
        Claude Haiku 4.5 (SSAFY GMS 엔드포인트)               │
        "vite" → ["vite", "프론트엔드", "React", "Vue", ...]  │
              │                                                │
              ▼                                                │
      [SQLite icontains OR 검색] ◀────────────────────────────┘
        Recruitment / Bootcamp / Certification / Competition
```

| 항목 | 내용 |
|------|------|
| 모델 | `claude-haiku-4-5-20251001` |
| 엔드포인트 | `https://gms.ssafy.io/gmsapi/api.anthropic.com/v1/messages` |
| 인증 | `.env`의 `GMS_KEY` |
| 캐시 | LocMemCache, TTL 24시간 |
| max_tokens | 300 (JSON 배열 반환용) |
| SearchView 표시 | 카테고리별 최대 3건 (`.slice(0, 3)`) |
| Label 뷰 표시 | 해당 카테고리 최대 50건 |

### 검색 카드 반환 필드

| 카테고리 | 반환 필드 | 카드 표시 |
|---------|----------|----------|
| jobs | `id`, `title`, `company__name`, `close_date` | 회사명(회색) / 공고명(굵게) / 마감일 |
| bootcamps | `id`, `title`, `company`, `close_date` | 운영사(회색) / 부트캠프명(굵게) / 마감일 |
| certifications | `id`, `jm_cd`, `name`, `series_name` | 계열명(회색) / 자격증명(굵게) / 시험일정 링크 |
| competitions | `id`, `title`, `host`, `keyword`, `start_date` | 주최사(회색) / 공모전명(굵게) / 분야 뱃지 / 시작일 |

---

## 데이터 모델

### Accounts
- **User**: AbstractUser 확장. `nickname`(unique), `gender`, `birth`, `profile_image`, `first_name`, `last_name`
- **Profile**: User 1:1. `education`, `certification`, `experience`, `language`, `preferred_location`, `preferred_position` (JSONField 배열), `desired_salary`

### Bootcamps
- **Bootcamp**: `title`, `region`(FK), `skills`(M2M), `expense`, `period`, `participation_time`, `program_process`, `recruitment_linkage`, `close_date`, `recruitment_url`(unique), `ai_fit_score`
- **Region**: `name`(unique)
- **Skill**: `name`(unique)

### Jobs
- **Company**: `name`, `industry`, `size`, `established_year`, `annual_sales`, `employee_count`, `homepage`, `logo_url`
- **Recruitment**: `company`(FK), `title`, `career`, `education`, `salary`, `employment_type`, `region`, `close_date`, `view_count`
- **RecruitmentDetail**: Recruitment 1:1. `job_description`, `qualification`, `working_hours`, `address`, `social_insurance` 등
- **HiringProcess**: `recruitment`(FK), `name`

### Certifications
- **Certification**: `jm_cd`(unique), `name`, `qualification_cl`, `major_job_field`, `minor_job_field`
- **Examination**: `certification`(FK), `plan_name`, `doc_reg_start/end`, `prac_reg_start/end`, `prac_pass_start/end` 등

### Community
- **Article**: `user`(FK), `label`(FK), `title`, `content`
- **Comment**: `user`(FK), `article`(FK), `content`

### Competitions
- **Competition**: `external_id`(unique), `title`, `host`, `start_date`, `end_date`, `keyword`, `homepage`, `thumbnail`, `description`(JSONField)

### Todos
- **Todo**: `user`(FK), `label`(FK), `todo`, `memo`, `is_completed`, `is_recommended`, `recommendation_score`

### Category (공통)
- **Category**: `name`
- **Label**: `name`

---

## 프론트엔드 페이지

| 경로 | 컴포넌트 | 상태 |
|------|----------|------|
| `/` | MainView | 완료 — 타이핑 효과(닉네임 포함 인사말, 90ms, 커서 깜빡임), 검색창 teal 그림자·최대 너비 600px, 예시 태그 pill 칩, 반응형(1200px: 이미지 400px·폰트 38px / 1000px 이하: 세로 배치), 1420px 이하 닉네임 줄 분리 |
| `/search` | SearchView | 완료 — AI 검색 결과 (채용공고·부트캠프·자격증·공모전) |
| `/signup` | SignupView | 완료 - 기본/추가 정보 섹션 구분, 실시간 유효성 검사, 생년월일 placeholder 숨김 |
| `/login` | LoginView | 완료 — 중앙 정렬, 로고 이미지, SCSS 스타일링 |
| `/profile/:username` | ProfileView | 완료 — 개인정보 탭 + 작성한 글 탭, 닉네임 표시, 투두 카드(teal, 프로그레스 바, 완료 수 표기), 희망 연봉 "만원" 표시, 작성한 글 카드 CommunityView 동일 스타일, 810px 반응형 |
| `/profile/:username/update` | UpdateProfileView | 완료 — 성/이름/프로필이미지(3:4·150×200px·border-radius 5%) + 배열 필드 태그 pill UI, 기존 데이터 pre-fill, 희망 연봉 "만원" 단위 표시, 태그 input 하단 배치 |
| `/bootcamp` | BootcampView | 완료 — 상단 SearchBox + 지역·카테고리 드롭다운 필터 |
| `/bootcamp/:bootcampPk` | BootcampDetailView | 완료 — 기술 스택 pill 뱃지 |
| `/jobs` | JobView | 완료 — 상단 SearchBox + 지역 드롭다운 필터 |
| `/jobs/:jobPk` | JobDetailView | 완료 |
| `/competition` | CompetitionView | 완료 — 상단 SearchBox |
| `/competition/:competitionPk` | CompetitionDetailView | 완료 |
| `/certification` | CertificationView | 완료 — 상단 SearchBox |
| `/certification/:jm_cd` | CertificationDetailView | 완료 |
| `/community` | CommunityView | 완료 — 카테고리 필터(고정 컬러), 댓글 수 우하단 SVG 아이콘, 닉네임·날짜 표시, 비로그인 블러 게이트, 810px 반응형 |
| `/community/article` | CommunityFormView | 완료 — UpdateProfileView 통일 디자인, 카테고리 선택, 이탈 방지 가드 |
| `/community/:pk` | CommunityDetailView | 완료 — 작성자 닉네임 표시, 목록으로 버튼, 제목 하단 구분선 |
| `/community/:pk/update` | CommunityUpdateView | 완료 — UpdateProfileView 통일 디자인 |
| `/calendar` | CalendarView | 완료 — 더미데이터 기반 마감일 배지, 호버 시 기간 하이라이트, TodoList 컴포넌트 분리 |

---

## 프론트엔드 상태 관리 (Pinia Stores)

| Store | 파일 | 주요 기능 |
|-------|------|-----------|
| userStore | `stores/userStore.js` | 토큰 영속 저장 (`persist: true`), 회원가입 후 토큰 즉시 저장, 로그인 후 프로필 자동 fetch(닉네임 유지), 로그아웃 시 nickname 초기화, 프로필 조회·수정 |
| bootcampStore | `stores/bootcampStore.js` | 목록 조회(`getBootcampList`), 단건 조회(`getBootcamp`), 지역·카테고리 필터(`selectedRegion`, `selectedCategory`, `setRegion`, `setCategory`), 옵션 목록 조회(`getRegions`, `getCategories`) |
| communityStore | `stores/communityStore.js` | 게시글 CRUD, 레이블 목록, 상세 조회 |
| comments | `stores/comments.js` | 댓글 작성(`commentCreate`), 댓글 삭제(`commentDelete`) |
| jobStore | `stores/jobStore.js` | 채용공고 목록/상세 조회, 지역 필터(`selectedRegion`, `setRegion`), 지역 목록 조회(`getRegions`) |
| certificationStore | `stores/certificationStore.js` | 자격증 목록/상세 조회 |
| competitionStore | `stores/competitionStore.js` | 공모전 목록/상세 조회 |
| todoStore | `stores/todoStore.js` | 할일 CRUD |
| searchStore | `stores/searchStore.js` | 검색어 바인딩(`keyword`), 검색 실행(`search`), 결과 저장(jobs·bootcamps·certifications·competitions) |

---

## 반응형 네비게이션

- **810px 이하**: 기존 nav 링크 숨김, 우상단 햄버거 버튼(≡) 노출
- **드롭다운 메뉴**: 클릭 시 상단에서 슬라이드다운 — 채용공고·자격증·부트캠프·공모전·커뮤니티 + 구분선 + 로그인/회원가입 (로그인 시 캘린더·프로필·로그아웃)
- **자동 닫힘**: `router.afterEach` 훅으로 페이지 이동 시 메뉴 자동 닫힘
- **프로필 드롭다운**: 로그인 시 닉네임 버튼 hover → "내 프로필" / "로그아웃" CSS :hover 방식 드롭다운 (fade + translateY 애니메이션)
- **전역 폰트**: Pretendard (npm 패키지) — `App.vue`에서 `@import` 후 `*` selector에 적용

---

## 주요 구현 패턴

- **AI 키워드 확장 검색**: `category/services.py`에서 Claude Haiku로 검색어를 최대 10개 관련 키워드로 확장 → SQLite `icontains` OR 필터로 4개 모델 동시 검색. 결과는 24시간 캐시(LocMemCache)
- **SearchBox 컴포넌트**: `components/common/SearchBox.vue`로 분리. `label` prop으로 동작 분기 — `null`이면 `/search`로 이동(전체 검색), 문자열이면 해당 카테고리 내 인라인 검색 후 `@results` emit. 검색 완료 후 input 자동 초기화. `extraParams` prop으로 region·category 필터를 검색 API에 함께 전달.
- **라벨 내 검색**: JobView·BootcampView·CertificationView·CompetitionView에서 SearchBox의 `@results` 이벤트를 수신해 List 컴포넌트에 `searchResults` prop으로 전달. 결과 0건이면 "키워드에 일치하는 정보가 없습니다." 출력.
- **검색 카드 일관성**: 각 카테고리 List 컴포넌트의 검색 결과 카드를 해당 카테고리 DetailCard 컴포넌트와 동일한 레이아웃·CSS로 통일.
- **드롭다운 필터**: JobView — 지역(앞 2글자 축약) 드롭다운. BootcampView — 지역·카테고리 드롭다운 2개. 뷰 진입 시 항상 전체로 초기화(store setup 단계에서 reset).
- **필터·검색 조합**: 필터 선택 후 검색(extraParams로 전달) 및 검색 후 필터 변경(JobView·BootcampView의 `watch`로 search API 재호출) 양방향 모두 지원. 검색 결과 모드가 아닐 때 필터 변경은 일반 목록을 재조회.
- **SearchView 인라인 검색**: SearchView 내 검색창에서 직접 검색 가능. 결과는 페이지 이동 없이 인라인 업데이트. 로딩 중 스피너 표시, 이전 결과 즉시 초기화.
- **비로그인 게이트**: 커뮤니티 목록에서 `v-else` 블러 오버레이 — 가짜 카드 blur + 로그인 안내 모달 카드
- **사용자 권한 UI**: 게시글/댓글에서 `article.username === userStore.username` 비교로 수정·삭제 버튼 조건부 렌더링
- **카테고리 필터**: 프론트엔드 `computed`로 `articleList`를 `selectedLabel`로 필터링
- **카테고리 고정 컬러**: `labelColorMap` 객체로 자격증·부트캠프·공모전·채용공고 배경색/글자색 고정, 필터 버튼도 동일 컬러 적용
- **닉네임 표시**: 커뮤니티 게시글·댓글·프로필 전 영역에서 `username` 대신 `nickname` 표시 — 백엔드 시리얼라이저에 `SerializerMethodField`(source=`user.nickname`) 추가
- **스토어 순환 의존 방지**: `communityStore` 내 `useUserStore()`를 함수 바디 안에서 호출
- **이미지/배열 전송**: 프로필 수정 시 `FormData` + `JSON.stringify` 배열 필드, 백엔드에서 `json.loads`로 파싱
- **실시간 유효성 검사**: SignupView에서 Vue `watch`로 각 필드 입력 즉시 검증 (형식·길이·일치 여부)
- **라우터 가드**: `beforeEach`에서 인증 필요 페이지 접근 시 LoginView로 리다이렉트
- **이탈 방지**: CommunityFormView에서 `onBeforeRouteLeave` + `watch([title, content])`로 작성 중 이탈 confirm

---

## 픽스처 로드

통합 픽스처 `backend/fixtures/total.json` (총 7,661개 레코드).

```bash
python manage.py loaddata ../fixtures/total.json
```

| 구성 | 레코드 수 |
|------|----------|
| 채용공고 (Recruitment) | 534개 (기존 484 + 테스트 50) |
| 자격증 (Certification) | 633개 (기존 613 + IT분야 20) |
| 부트캠프 (Bootcamp) | 447개 |
| 공모전 (Competition) | 426개 |
| 기타 (region, skill, category 등) | 나머지 |

테스트 데이터 커버 분야: 프론트엔드 · 백엔드 · 데이터 엔지니어링 · AI/ML · UI/UX 디자인 · 클라우드/DevOps · 정보보안 · 모바일 앱 · 게임 개발 · 회계/재무
- **로그인 후 닉네임 유지**: `userStore.logIn()` 성공 후 `getProfile()`을 호출해 `nickname` 즉시 설정, 로그아웃 시 `nickname = null` 초기화
- **투두 카드 프로그레스**: `todoStore.completedCount / todoStore.todoList.length`로 진행률 계산, CSS width 바인딩으로 애니메이션
- **실시간 유효성 검사**: SignupView에서 Vue `watch`로 각 필드 입력 즉시 검증 (형식·길이·일치 여부), 서버 에러는 catch에서 병합 표시
- **로그인 에러 표시**: LoginView에서 `non_field_errors` 응답을 "아이디 또는 비밀번호가 잘못되었습니다." 고정 문구로 표시
- **라우터 가드**: `beforeEach`에서 인증 필요 페이지 접근 시 LoginView로 리다이렉트
- **라우터 name 통일**: 전체 프론트엔드에서 `to="/path"` 대신 `{ name: 'RouteName' }` 방식으로 통일 — 경로 변경 시 한 곳(router/index.js)만 수정하면 됨
- **캘린더 이벤트 표시**: 더미데이터 기반 마감일 배지 + 호버 시 이벤트 기간 전체 하이라이트 (`isInRange` computed)
- **TodoList 슬림 UI**: `height: 32px` 고정 + `white-space: nowrap`으로 버튼 텍스트 줄바꿈 방지, wrapper에 `display: flex; flex-direction: column`으로 `margin-top: auto` 정상 동작
- **이탈 방지**: CommunityFormView에서 `onBeforeRouteLeave` + `watch([title, content])`로 작성 중 이탈 confirm (Vue Router 4 `return` 패턴)
- **반응형 기준 통일**: 전체 브레이크포인트 810px — 모든 뷰(MainView·ProfileView·CommunityView·UpdateProfileView 등) 및 AppNav 동일 기준 적용
- **타이핑 효과**: MainView 헤딩에서 `setInterval`로 한 글자씩 출력, `route.fullPath` watch로 페이지 진입 시마다 재시작, `v-html` + `:deep()` 으로 scoped 환경에서 동적 span 색상 적용
- **반응형 JS**: `window.innerWidth`를 `ref`로 래핑 + `resize` 이벤트로 반응형 — 1420px 이하에서 닉네임 줄 분리를 JS 단에서 처리(`displayedHtml` computed 내 문자열 조작)

---

## 픽스처 로드

모든 앱의 fixture를 `backend/fixtures/total.json` 하나로 통합했습니다.

```bash
# 통합 로드 (권장)
python manage.py migrate
python manage.py loaddata total.json
```

외래 키 오류 발생 시 개별 순서대로 로드:

```bash
python manage.py loaddata category.json label.json region.json skill.json bootcamp.json jobs.json competitions.json certifications.json examinations.json
```

로드 순서: category → label → region → skill → bootcamp → jobs → competitions → certifications → examinations

---

## 개발 예정 기능

- **AI 적합도 점수**: 사용자 프로필과 채용공고/부트캠프를 비교해 fit 점수 도출 (`ai_score` 앱)
- **캘린더 연동**: 자격증 시험 일정·공채 마감일 자동 등록

---

## UI/UX 개선 이력

### 카테고리 페이지 통합 디자인 (채용공고·자격증·부트캠프·공모전)

#### 검색/필터 영역
- 셀렉트박스 + 검색창을 한 줄(`flex-direction: row`)로 배치, 가운데 정렬
- 채용공고: 지역 셀렉트박스 1개 + SearchBox
- 부트캠프: 지역·카테고리 셀렉트박스 2개 + SearchBox
- 자격증·공모전: SearchBox만 (가운데 정렬)
- SearchBox 디자인 통일 — `border: 2px solid #2ab59e`, `border-radius: 50px`, 박스 그림자 제거, 돋보기 아이콘 제거, placeholder `"관심 직무를 검색해보세요."`

#### 카드 레이아웃 통일
모든 카테고리 카드(목록·검색 결과·길라잡이 픽)를 동일한 `card-top / card-bottom` 구조로 통일:

| 영역 | 채용공고 | 자격증 | 부트캠프 | 공모전 |
|------|---------|--------|---------|--------|
| card-top 상단 (14px 회색) | 회사명 | 계열명 | 운영사 | 주최사 |
| card-top 중단 (17px 굵게) | 공고 타이틀 | 자격증명 | 부트캠프명 | 공모전명 |
| card-top 하단 (13px) | 경력 | — | — | 키워드(회색) |
| card-bottom 좌 (14px teal) | 카테고리 | 시험 일정 버튼 | 카테고리 | 카테고리 |
| card-bottom 우 (14px 회색) | 마감일 | — | 마감일 | 시작일 |

- 모든 카드 `height: 200px` 고정, `box-sizing: border-box`, `justify-content: space-between`
- 자격증 "시험 일정 보러가기" 버튼: 초록색(`#2ab59e`) 배경, `border-radius: 7px`

#### 길라잡이 픽 (`gillajobi_pick.vue`)
- 카드 3개를 가로(`flex-direction: row`) 배치
- 순위 뱃지(1·2·3)를 카드 우상단에 배치
- 카드 하단 좌측에 카테고리명 표시
- 컴포넌트 타이틀 동적 변환: `type` prop → `채용공고 / 자격증 / 부트캠프 / 공모전`
- 810px 이하: `flex-direction: column` 반응형 적용
- 백엔드 `jobs/views.py`, `bootcamps/views.py`, `competitions/views.py`의 `top3` 뷰에 `category__name` 필드 추가

#### AI 추천 컴포넌트 (`AiRecommend.vue`)
- 4개 카테고리 뷰 공통으로 신규 생성
- 컴포넌트 타이틀 동적: `✨ AI 추천 채용공고 / 자격증 / 부트캠프 / 공모전`
- 배경색 없음

#### 검색·필터 시 AI 추천/길라잡이 픽 자동 숨김
- 채용공고: 검색 결과가 있거나(`searchResults !== null`) 지역 필터 선택 시 숨김
- 자격증·공모전: 검색 결과가 있을 때 숨김
- 부트캠프: 검색 결과가 없고 지역·카테고리 필터도 미선택인 경우에만 표시

#### 목록 섹션 타이틀 및 검색 결과 표시
- 기본 상태: "전체 채용공고 / 전체 자격증 / 전체 부트캠프 / 전체 공모전" 타이틀 + teal 구분선
- 검색/필터 후: `"키워드" 검색 결과 N건` (font-size: 1rem, color: #666)
- 부트캠프 필터 레이블: 지역 + 카테고리 + 키워드를 `" / "`로 조합 (`filterLabel` computed)
- 결과 없음: `"키워드"에 일치하는 정보가 없습니다.` (font-size: 1.2rem, 중앙 정렬)

#### TopButton 컴포넌트 (`TopButton.vue`) 신규
- 4개 카테고리 뷰에 공통 추가
- 스크롤 300px 초과 시 노출, 클릭 시 최상단 부드럽게 이동
- 스타일: teal 테두리 원형 + SVG 위 화살표, 우하단 고정(40px)

#### AppNav 탭 동일 페이지 새로고침
- 이미 해당 페이지에 있는 탭 클릭 시 `router.go(0)`으로 페이지 새로고침
- 다른 페이지로 이동 시 기존 `router.push` 유지
- 모바일 드롭다운 링크도 동일 로직 적용
- 전체 폰트 크기 소폭 증가: nav-link 1rem, btn-calendar/btn-signup 0.95rem, nav-username 1rem, mobile-link 1.02rem
