import json
import os
import requests

import django.db
from django.db.models import Q
from dotenv import load_dotenv

from category.services import expand_keywords

load_dotenv()

GMS_URL = "https://gms.ssafy.io/gmsapi/api.anthropic.com/v1/messages"
LOG_FILE = os.path.join(os.path.dirname(__file__), 'ai_score.log')


def _log(msg):
    import datetime
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


CONTENT_TYPES = ['bootcamp', 'job', 'certification', 'competition']


# ── 공개 API ──────────────────────────────────────────────────────────────────

def compute_scores_for_user(user):
    """백그라운드 스레드 진입점. 4카테고리 순차 계산 후 DB 저장."""
    import traceback as _tb
    _log(f"START user={user.id}")
    try:
        django.db.close_old_connections()

        profile = user.profile
        _log(f"profile loaded: empty={_is_profile_empty(profile)}")
        if _is_profile_empty(profile):
            return

        profile_summary = _build_profile_summary(profile)
        keywords = _expand_profile_keywords(profile)
        _log(f"keywords: {keywords}")

        for ct in CONTENT_TYPES:
            try:
                _compute_single_category(user, profile_summary, keywords, ct)
            except Exception as e:
                _log(f"{ct} FAILED: {type(e).__name__}: {e}\n{_tb.format_exc()}")
    except Exception as e:
        _log(f"FATAL: {type(e).__name__}: {e}\n{_tb.format_exc()}")
    _log("END")


def get_recommendations(user, content_type):
    """DB에서 상위 3건 반환. status 포함."""
    from .models import FitScore

    profile = user.profile
    if _is_profile_empty(profile):
        return {'type': content_type, 'status': 'empty_profile', 'items': []}

    # score >= 0 인 실제 결과
    scores = (
        FitScore.objects
        .filter(user=user, content_type=content_type, score__gte=0)
        .order_by('-score')[:3]
    )

    if scores:
        items = [_enrich_score(s) for s in scores]
        return {'type': content_type, 'status': 'ready', 'items': items}

    # score=-1 sentinel → 계산 완료, 결과 없음
    has_sentinel = FitScore.objects.filter(
        user=user, content_type=content_type, score=-1
    ).exists()
    if has_sentinel:
        return {'type': content_type, 'status': 'no_match', 'items': []}

    return {'type': content_type, 'status': 'computing', 'items': []}


def get_score_detail(user, content_type, object_id):
    """단건 점수 조회. 없으면 None 반환."""
    from .models import FitScore

    try:
        fs = FitScore.objects.get(
            user=user, content_type=content_type, object_id=object_id)
        return {'score': fs.score, 'reason': fs.reason}
    except FitScore.DoesNotExist:
        return {'score': None}


def invalidate_user_scores(user):
    """프로필 변경 시 기존 점수 전체 삭제."""
    from .models import FitScore
    FitScore.objects.filter(user=user).delete()


# ── 내부 함수 ─────────────────────────────────────────────────────────────────

def _is_profile_empty(profile):
    return not any([
        profile.preferred_position,
        profile.experience,
        profile.education,
    ])


def _build_profile_summary(profile):
    return {
        'preferred_position': profile.preferred_position or [],
        'experience': profile.experience or [],
        'education': profile.education or [],
        'certification': profile.certification or [],
        'language': profile.language or [],
        'preferred_location': profile.preferred_location or [],
        'desired_salary': profile.desired_salary or '',
    }


def _expand_profile_keywords(profile):
    base = (profile.preferred_position or []) + (profile.experience or [])
    if not base:
        return []
    query = ' '.join(base[:5])
    try:
        expanded = expand_keywords(query)
        # 원본 키워드를 항상 포함하여 DB 매칭 안정성 확보
        seen = set()
        result = []
        for kw in (base + expanded):
            if kw not in seen:
                seen.add(kw)
                result.append(kw)
        return result
    except Exception:
        return base


def _compute_single_category(user, profile_summary, keywords, content_type):
    from .models import FitScore

    django.db.close_old_connections()
    candidates = _prefetch_candidates(keywords, profile_summary, content_type)
    if not candidates:
        # 후보 없음을 명시적으로 기록 (status=computing이 무한 지속되는 것 방지)
        FitScore.objects.update_or_create(
            user=user, content_type=content_type, object_id=0,
            defaults={'score': -1, 'reason': ''},
        )
        return

    scored = _batch_score(profile_summary, content_type, candidates)
    if not scored:
        FitScore.objects.update_or_create(
            user=user, content_type=content_type, object_id=0,
            defaults={'score': -1, 'reason': ''},
        )
        return

    for item in scored:
        FitScore.objects.update_or_create(
            user=user,
            content_type=content_type,
            object_id=item['id'],
            defaults={
                'score': item['score'],
                'reason': item.get('reason', '')[:200],
            },
        )


def _prefetch_candidates(keywords, profile_summary, content_type):
    preferred_locations = profile_summary.get('preferred_location', [])
    location_prefixes = [loc[:2]
                         for loc in preferred_locations if len(loc) >= 2]

    if content_type == 'bootcamp':
        return _candidates_bootcamp(keywords)
    elif content_type == 'job':
        return _candidates_job(keywords, location_prefixes)
    elif content_type == 'certification':
        return _candidates_certification(keywords)
    elif content_type == 'competition':
        return _candidates_competition(keywords)
    return []


def _candidates_bootcamp(keywords):
    from bootcamps.models import Bootcamp

    if keywords:
        q = Q()
        for kw in keywords:
            q |= Q(skills__name__icontains=kw) | Q(
                category__name__icontains=kw)
        qs = Bootcamp.objects.filter(q).distinct()[:15]
    else:
        qs = Bootcamp.objects.order_by('-created_at')[:15]

    result = []
    for b in qs:
        result.append({
            'id': b.id,
            'title': b.title,
            'company': b.company,
            'region': b.region.name if b.region else '',
            'category': b.category.name if b.category else '',
            'skills': list(b.skills.values_list('name', flat=True)),
            'close_date': str(b.close_date) if b.close_date else '',
        })
    return result


def _candidates_job(keywords, location_prefixes):
    from jobs.models import Recruitment

    q = Q()
    for kw in keywords:
        q |= Q(category__name__icontains=kw) | Q(title__icontains=kw)

    base_qs = Recruitment.objects.select_related(
        'company', 'category', 'detail')

    if q:
        if location_prefixes:
            lq = Q()
            for prefix in location_prefixes:
                lq |= Q(region__startswith=prefix)
            qs = base_qs.filter(q & lq).distinct()[:15]
            if not qs.exists():
                qs = base_qs.filter(q).distinct()[:15]
        else:
            qs = base_qs.filter(q).distinct()[:15]
    else:
        qs = base_qs.order_by('-id')[:15]

    result = []
    for r in qs:
        detail = getattr(r, 'detail', None)
        result.append({
            'id': r.id,
            'title': r.title,
            'company': r.company.name if r.company else '',
            'region': r.region or '',
            'category': r.category.name if r.category else '',
            'career': r.career or '',
            'close_date': str(r.close_date) if r.close_date else '',
            'job_description': (detail.job_description or '')[:300] if detail else '',
            'qualification': (detail.qualification or '')[:200] if detail else '',
        })
    return result


def _candidates_certification(keywords):
    from certifications.models import Certification

    if keywords:
        q = Q()
        for kw in keywords:
            q |= Q(major_job_field__icontains=kw) | Q(
                minor_job_field__icontains=kw) | Q(name__icontains=kw)
        qs = Certification.objects.filter(q).distinct()[:15]
    else:
        qs = Certification.objects.order_by('-id')[:15]

    return [
        {
            'id': c.id,
            'jm_cd': c.jm_cd,
            'name': c.name,
            'series_name': c.series_name,
            'major_job_field': c.major_job_field,
            'minor_job_field': c.minor_job_field,
        }
        for c in qs
    ]


def _candidates_competition(keywords):
    from competitions.models import Competition

    if keywords:
        q = Q()
        for kw in keywords:
            q |= Q(keyword__icontains=kw) | Q(title__icontains=kw)
        qs = Competition.objects.filter(q).distinct()[:15]
    else:
        qs = Competition.objects.order_by('-id')[:15]

    return [
        {
            'id': c.id,
            'title': c.title,
            'host': c.host,
            'keyword': c.keyword,
            'start_date': str(c.start_date) if c.start_date else '',
            'end_date': str(c.end_date) if c.end_date else '',
        }
        for c in qs
    ]


def _batch_score(profile_summary, content_type, candidates):
    type_label = {
        'bootcamp': '부트캠프',
        'job': '채용공고',
        'certification': '자격증',
        'competition': '공모전',
    }[content_type]

    prompt = f"""너는 취업 플랫폼 AI 매칭 엔진이야.

사용자 프로필:
- 희망 직무: {profile_summary['preferred_position']}
- 경력/기술: {profile_summary['experience']}
- 학력: {profile_summary['education']}
- 보유 자격증: {profile_summary['certification']}
- 선호 지역: {profile_summary['preferred_location']}
- 희망 연봉: {profile_summary['desired_salary']}

아래 {type_label} 목록을 사용자와의 적합도 기준으로 0~100점 평가해줘.
(80~100: 매우 적합 / 60~79: 적합 / 40~59: 보통 / 0~39: 낮음)

{json.dumps(candidates, ensure_ascii=False)}

JSON 배열만 반환. 다른 텍스트 없이.
형식: [{{"id": 1, "score": 85, "reason": "백엔드 희망 직무와 정확히 일치"}}]"""

    import time
    for attempt in range(2):
        try:
            text = _call_claude(prompt)
            result = _parse_scores(text)
            if result:
                _log(
                    f"OK ({content_type}) attempt={attempt}: {len(result)} items")
                return result
            # Claude가 빈 배열 또는 파싱 불가 응답을 반환한 경우
            _log(
                f"PARSE_EMPTY ({content_type}) attempt={attempt}: raw={repr(text[:300])}")
            if attempt == 0:
                time.sleep(2)
        except Exception as e:
            _log(
                f"EXCEPTION ({content_type}) attempt={attempt}: {type(e).__name__}: {e}")
            if attempt == 0:
                time.sleep(3)
    return []


def _call_claude(prompt):
    headers = {
        "x-api-key": os.getenv("GMS_KEY"),
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(GMS_URL, headers=headers, json=body, timeout=20)
    resp.raise_for_status()
    return resp.json()["content"][0]["text"].strip()


def _parse_scores(text):
    import re

    def _extract_items(data):
        if not isinstance(data, list):
            return []
        return [
            {'id': item['id'], 'score': int(
                item['score']), 'reason': item.get('reason', '')}
            for item in data
            if isinstance(item, dict) and 'id' in item and 'score' in item
        ]

    # 1) 마크다운 코드블록 안에서 JSON 추출
    if '```' in text:
        for part in text.split('```')[1::2]:
            if part.startswith('json'):
                part = part[4:]
            try:
                items = _extract_items(json.loads(part.strip()))
                if items:
                    return items
            except (json.JSONDecodeError, ValueError):
                continue

    # 2) 텍스트 전체 직접 파싱
    try:
        items = _extract_items(json.loads(text))
        if items:
            return items
    except (json.JSONDecodeError, ValueError):
        pass

    # 3) 텍스트 내 JSON 배열 패턴 검색
    match = re.search(r'\[[\s\S]*?\]', text)
    if match:
        try:
            items = _extract_items(json.loads(match.group()))
            if items:
                return items
        except (json.JSONDecodeError, ValueError):
            pass

    return []


def _enrich_score(fit_score):
    """FitScore 인스턴스에 해당 아이템의 상세 정보를 붙여 반환."""
    ct = fit_score.content_type
    oid = fit_score.object_id
    base = {'id': oid, 'score': fit_score.score, 'reason': fit_score.reason}

    try:
        if ct == 'bootcamp':
            from bootcamps.models import Bootcamp
            b = Bootcamp.objects.select_related('category').get(pk=oid)
            base.update({'title': b.title, 'company': b.company,
                         'close_date': str(b.close_date) if b.close_date else '',
                         'category': b.category.name if b.category else ''})
        elif ct == 'job':
            from jobs.models import Recruitment
            r = Recruitment.objects.select_related(
                'company', 'category').get(pk=oid)
            base.update({'title': r.title, 'company': r.company.name if r.company else '',
                         'close_date': str(r.close_date) if r.close_date else '',
                         'category': r.category.name if r.category else ''})
        elif ct == 'certification':
            from certifications.models import Certification
            c = Certification.objects.get(pk=oid)
            base.update({'title': c.name, 'company': c.series_name,
                         'jm_cd': c.jm_cd, 'category': c.major_job_field})
        elif ct == 'competition':
            from competitions.models import Competition
            comp = Competition.objects.get(pk=oid)
            base.update({'title': comp.title, 'company': comp.host,
                         'close_date': str(comp.end_date) if comp.end_date else '',
                         'category': comp.keyword})
    except Exception:
        pass

    return base
