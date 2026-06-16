import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from .models import Certification, Examination

load_dotenv()


# 한국산업인력공단_국가자격 종목 목록 정보_20241231
def get_certification_data():
    SERVICE_KEY = os.getenv('SERVICE_KEY')
    CER_API_URL = os.getenv('CER_API_URL')

    params = {'serviceKey': SERVICE_KEY, '_type': 'json'}
    response = requests.get(CER_API_URL, params=params) 
    response.raise_for_status()

    items = response.json().get('response', {}).get('body', {}).get('items', {}).get('item', [])
    if isinstance(items, dict): # 결과가 1건일 때 dict로 오는 경우 처리
        items = [items]

    for item in items:
        Certification.objects.update_or_create(
            jm_cd=item.get('jmcd', ''),
            defaults={
                'name': item.get('jmfldnm', ''),
                'qualification_cl': item.get('qualgbnm', ''),
                'series_name': item.get('seriesnm', ''),
                'major_job_field': item.get('obligfldnm', ''),
                'minor_job_field': item.get('mdobligfldnm', ''),
            }
        )


def _parse_date(value):
    if not value:
        return None

    value = str(value).strip()
    for date_format in ('%Y%m%d', '%Y-%m-%d'):
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            pass

    return None


# 한국산업인력공단_국가기술자격 종목별 시험정보
# : 현재연도의 국가기술자격 종목별 시험 시행일정 조회
def get_examination_data(jm_cd):
    SERVICE_KEY = os.getenv('SERVICE_KEY')
    EXAM_API_URL = os.getenv('EXAM_API_URL')

    params = {'serviceKey': SERVICE_KEY, 'jmCd': jm_cd, '_type': 'json'}
    response = requests.get(EXAM_API_URL, params=params)
    response.raise_for_status()

    items_raw = response.json().get('response', {}).get('body', {}).get('items') or {}
    if not isinstance(items_raw, dict):
        return
    
    items = items_raw.get('item', [])
    if isinstance(items, dict):
        items = [items]

    certification = Certification.objects.get(jm_cd=jm_cd)
    for item in items:
        Examination.objects.update_or_create(
            certification=certification,
            plan_name=item.get('implplannm', ''),
            defaults={
                'jm_name': item.get('jmfldnm', ''),
                'doc_reg_start': _parse_date(item.get('docregstartdt')),
                'doc_reg_end': _parse_date(item.get('docregenddt')),
                'doc_exam_start': _parse_date(item.get('docexamstartdt')),
                'doc_exam_end': _parse_date(item.get('docexamenddt')),
                'doc_pass_dt': _parse_date(item.get('docpassdt')),
                'doc_submit_start': _parse_date(item.get('docsubmitstartdt')),
                'doc_submit_end': _parse_date(item.get('docsubmitenddt')),
                'prac_reg_start': _parse_date(item.get('pracregstartdt')),
                'prac_reg_end': _parse_date(item.get('pracregenddt')),
                'prac_exam_start': _parse_date(item.get('pracexamstartdt')),
                'prac_exam_end': _parse_date(item.get('pracexamenddt')),
                'prac_pass_start': _parse_date(item.get('pracpassstartdt')),
                'prac_pass_end': _parse_date(item.get('pracpassenddt')),
            }
        )


def sync_all_examinations():
    jm_cds = Certification.objects.values_list('jm_cd', flat=True)
    for jm_cd in jm_cds:
        try:
            get_examination_data(jm_cd)
        except Exception as e:
            print(f'{jm_cd} 동기화 실패: {e}')


# 한국산업인력공단_기사 종목별 시험정보 현황_20241231
# def get_gisa_data():
#     SERVICE_KEY = os.getenv('SERVICE_KEY')
#     # url = 'https://api.odcloud.kr/api/3073409/v1/uddi:1d82aa67-c306-4970-a870-bc18f6d31a9a'
#     url = 'http://apis.data.go.kr/B490007/qualExamSchd/getQualExamSchdList'
#     params ={'serviceKey' : SERVICE_KEY, '_type': 'json'}
#     # params ={'serviceKey' : SERVICE_KEY, 'seriesCd' : '41', '_type': 'json'}

#     response = requests.get(url, params=params)
#     print(response.json())  # 실제 응답 원문으로 필드명 직접 확인

# get_examination_data()