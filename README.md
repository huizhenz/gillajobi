# 길라잡이 (Gillajobi)

취업 준비생을 위한 채용 정보 통합 플랫폼. 채용공고, 부트캠프, 자격증, 공모전 정보를 한 곳에서 제공한다.

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | Django 5.2, Django REST Framework, dj-rest-auth, django-allauth |
| Frontend | Vue 3, Pinia, Vue Router, Axios, SCSS, Pretendard 폰트(npm) |
| DB | SQLite |
| 인증 | Token Authentication |
| 데이터 수집 | Requests, BeautifulSoup4 (크롤링) |

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
│   ├── category/             # 공통 카테고리 & 라벨
│   └── ai_score/             # AI 적합도 점수 (개발 예정)
│
└── frontend/                 # Vue.js 클라이언트
    └── src/
        ├── views/            # 페이지 컴포넌트
        ├── components/       # 재사용 UI 컴포넌트
        ├── stores/           # Pinia 상태 관리
        └── router/           # Vue Router 설정
```

---

## 실행 방법

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver        # http://127.0.0.1:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173
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
| GET | `/bootcamps/` | 부트캠프 목록 |
| GET | `/bootcamps/<bootcamp_pk>/` | 부트캠프 상세 |
| GET | `/bootcamps/fetch/` | 외부 사이트(boottent.com) 크롤링 후 저장 (`?page=N` 옵션) |

### Jobs
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/jobs/` | 채용공고 목록 |
| GET | `/jobs/<job_pk>/` | 채용공고 상세 |
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

### Todos
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET / POST | `/todos/` | 할일 목록 / 생성 |
| PUT / DELETE | `/todos/<id>/` | 할일 수정 / 삭제 |

---

## 데이터 모델

### Accounts
- **User**: AbstractUser 확장. `nickname`(unique), `gender`, `birth`, `profile_image`, `first_name`, `last_name`
- **Profile**: User 1:1. `education`, `certification`, `experience`, `language`, `preferred_location`, `preferred_position` (JSONField 배열 — 여러 항목 저장), `desired_salary`(TextField)

### Bootcamps
- **Bootcamp**: `title`, `region`(FK), `skills`(M2M), `expense`, `period`, `participation_time`, `program_process`, `recruitment_linkage`, `close_date`, `close_date_text`, `recruitment_url`(unique), `ai_fit_score`
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
| `/signup` | SignupView | 완료 |
| `/login` | LoginView | 완료 — 중앙 정렬, 로고 이미지, SCSS 스타일링 |
| `/signup` | SignupView | 완료 — 기본/추가 정보 섹션 구분, 실시간 유효성 검사, 생년월일 placeholder 숨김 |
| `/profile/:username` | ProfileView | 완료 — 개인정보 탭 + 작성한 글 탭, 닉네임 표시, 투두 카드(teal, 프로그레스 바, 완료 수 표기), 희망 연봉 "만원" 표시, 작성한 글 카드 CommunityView 동일 스타일, 810px 반응형 |
| `/profile/:username/update` | UpdateProfileView | 완료 — 성/이름/프로필이미지(3:4·150×200px·border-radius 5%) + 배열 필드 태그 pill UI, 기존 데이터 pre-fill, 희망 연봉 "만원" 단위 표시, 태그 input 하단 배치 |
| `/bootcamp` | BootcampView | 완료 |
| `/bootcamp/:bootcampPk` | BootcampDetailView | 완료 — 기술 스택 pill 뱃지 |
| `/jobs` | JobView | 완료 |
| `/jobs/:jobPk` | JobDetailView | 완료 |
| `/competition` | CompetitionView | 완료 |
| `/competition/:competitionPk` | CompetitionDetailView | 완료 |
| `/certification` | CertificationView | 완료 |
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
| bootcampStore | `stores/bootcampStore.js` | 목록 조회(`getBootcampList`), 단건 조회(`getBootcamp`) |
| communityStore | `stores/communityStore.js` | 게시글 CRUD, 레이블 목록, 상세 조회 |
| comments | `stores/comments.js` | 댓글 작성(`commentCreate`), 댓글 삭제(`commentDelete`) |
| jobStore | `stores/jobStore.js` | 채용공고 목록/상세 조회 |
| certificationStore | `stores/certificationStore.js` | 자격증 목록/상세 조회 |
| competitionStore | `stores/competitionStore.js` | 공모전 목록/상세 조회 |
| todoStore | `stores/todoStore.js` | 할일 CRUD, ProfileView onMounted에서 자동 로드 |

---

---

## 반응형 네비게이션

- **810px 이하**: 기존 nav 링크 숨김, 우상단 햄버거 버튼(≡) 노출
- **드롭다운 메뉴**: 클릭 시 상단에서 슬라이드다운 — 채용공고·자격증·부트캠프·공모전·커뮤니티 + 구분선 + 로그인/회원가입 (로그인 시 캘린더·프로필·로그아웃)
- **자동 닫힘**: `router.afterEach` 훅으로 페이지 이동 시 메뉴 자동 닫힘
- **프로필 드롭다운**: 로그인 시 닉네임 버튼 hover → "내 프로필" / "로그아웃" CSS :hover 방식 드롭다운 (fade + translateY 애니메이션)
- **전역 폰트**: Pretendard (npm 패키지) — `App.vue`에서 `@import` 후 `*` selector에 적용

---

## 주요 구현 패턴

- **비로그인 게이트**: 커뮤니티 목록에서 `v-else` 블러 오버레이 — 가짜 카드 blur + 로그인 안내 모달 카드
- **사용자 권한 UI**: 게시글/댓글에서 `article.username === userStore.username` 비교로 수정·삭제 버튼 조건부 렌더링
- **카테고리 필터**: 프론트엔드 `computed`로 `articleList`를 `selectedLabel`로 필터링
- **카테고리 고정 컬러**: `labelColorMap` 객체로 자격증·부트캠프·공모전·채용공고 배경색/글자색 고정, 필터 버튼도 동일 컬러 적용
- **닉네임 표시**: 커뮤니티 게시글·댓글·프로필 전 영역에서 `username` 대신 `nickname` 표시 — 백엔드 시리얼라이저에 `SerializerMethodField`(source=`user.nickname`) 추가
- **스토어 순환 의존 방지**: `communityStore` 내 `useUserStore()`를 함수 바디 안에서 호출
- **프로필 내 작성 글**: `communityStore.articleList.filter(a => a.username === userStore.username)` — 별도 API 없이 프론트 필터링
- **이미지/배열 전송**: 프로필 수정 시 `FormData` + `JSON.stringify` 배열 필드, 백엔드에서 `json.loads`로 파싱
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