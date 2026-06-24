# 길라잡이 (Gillajobi)

취업 준비생을 위한 채용 정보 통합 플랫폼. 채용공고, 부트캠프, 자격증, 공모전 정보를 한 곳에서 제공한다.

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | Django 5.2, Django REST Framework, dj-rest-auth, django-allauth |
| Frontend | Vue 3, Pinia, Vue Router, Axios, SCSS |
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
| `/` | MainView | 완료 |
| `/signup` | SignupView | 완료 |
| `/login` | LoginView | 완료 |
| `/profile/:username` | ProfileView | 완료 — 개인정보 탭 + 작성한 글 탭 (카드 레이아웃) |
| `/profile/:username/update` | UpdateProfileView | 완료 — 성/이름/프로필이미지 + 배열 필드 태그 pill UI (추가·삭제), 기존 데이터 자동 pre-fill |
| `/bootcamp` | BootcampView | 완료 |
| `/bootcamp/:bootcampPk` | BootcampDetailView | 완료 — 기술 스택 pill 뱃지 |
| `/jobs` | JobView | 완료 |
| `/jobs/:jobPk` | JobDetailView | 완료 |
| `/competition` | CompetitionView | 완료 |
| `/competition/:competitionPk` | CompetitionDetailView | 완료 |
| `/certification` | CertificationView | 완료 |
| `/certification/:jm_cd` | CertificationDetailView | 완료 |
| `/community` | CommunityView | 완료 — 카테고리 필터, 댓글 수 표시, 비로그인 블러 게이트 |
| `/community/article` | CommunityFormView | 완료 — 카테고리 선택 포함 |
| `/community/:pk` | CommunityDetailView | 완료 — 작성자 본인만 수정/삭제 |
| `/community/:pk/update` | CommunityUpdateView | 완료 |
| `/calendar` | CalendarView | 완료 |

---

## 프론트엔드 상태 관리 (Pinia Stores)

| Store | 파일 | 주요 기능 |
|-------|------|-----------|
| userStore | `stores/userStore.js` | 토큰 영속 저장 (`persist: true`), 회원가입 후 토큰 즉시 저장, 로그인/로그아웃, 프로필 조회(`getProfile`)·수정, 에러 re-throw |
| bootcampStore | `stores/bootcampStore.js` | 목록 조회(`getBootcampList`), 단건 조회(`getBootcamp`) |
| communityStore | `stores/communityStore.js` | 게시글 CRUD, 레이블 목록, 상세 조회 |
| comments | `stores/comments.js` | 댓글 작성(`commentCreate`), 댓글 삭제(`commentDelete`) |
| jobStore | `stores/jobStore.js` | 채용공고 목록/상세 조회 |
| certificationStore | `stores/certificationStore.js` | 자격증 목록/상세 조회 |
| competitionStore | `stores/competitionStore.js` | 공모전 목록/상세 조회 |
| todoStore | `stores/todoStore.js` | 할일 CRUD |

---

---

## 주요 구현 패턴

- **비로그인 게이트**: 커뮤니티 목록에서 `v-else` 블러 오버레이 — 가짜 카드 blur + 로그인 안내 모달 카드
- **사용자 권한 UI**: 게시글/댓글에서 `article.username === userStore.username` 비교로 수정·삭제 버튼 조건부 렌더링
- **카테고리 필터**: 프론트엔드 `computed`로 `articleList`를 `selectedLabel`로 필터링
- **스토어 순환 의존 방지**: `communityStore` 내 `useUserStore()`를 함수 바디 안에서 호출
- **프로필 내 작성 글**: `communityStore.articleList.filter(a => a.username === userStore.username)` — 별도 API 없이 프론트 필터링
- **이미지/배열 전송**: 프로필 수정 시 `FormData` + `JSON.stringify` 배열 필드, 백엔드에서 `json.loads`로 파싱
- **실시간 유효성 검사**: SignupView에서 Vue `watch`로 각 필드 입력 즉시 검증 (형식·길이·일치 여부), 서버 에러는 catch에서 병합 표시
- **로그인 에러 표시**: LoginView에서 `non_field_errors` 응답을 "아이디 또는 비밀번호가 잘못되었습니다." 고정 문구로 표시
- **라우터 가드**: `beforeEach`에서 인증 필요 페이지 접근 시 LoginView로 리다이렉트
- **이탈 방지**: CommunityFormView에서 `onBeforeRouteLeave` + `watch([title, content])`로 작성 중 이탈 confirm (Vue Router 4 `return` 패턴)

---

## 픽스처 로드

모든 앱의 fixture를 `backend/fixtures.json` 하나로 통합했습니다 (총 7,172개 레코드).

```bash
python manage.py loaddata fixtures.json
```

로드 순서: category → label → region → skill → jobs → bootcamp → certifications → examinations → competitions

---

## 개발 예정 기능

- **AI 적합도 점수**: 사용자 프로필과 채용공고/부트캠프를 비교해 fit 점수 도출 (`ai_score` 앱)
- **캘린더 연동**: 자격증 시험 일정·공채 마감일 자동 등록