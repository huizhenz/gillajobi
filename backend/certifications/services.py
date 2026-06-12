import os

import requests
from dotenv import load_dotenv

from .models import Certification


load_dotenv()

def get_certification_data():
    API_URL = os.getenv('API_URL')
    SERVICE_KEY = os.getenv('SERVICE_KEY')

    params ={'serviceKey' : SERVICE_KEY, '_type': 'json'}
    response = requests.get(API_URL, params=params) 
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