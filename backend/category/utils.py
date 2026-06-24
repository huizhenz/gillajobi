import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None: # 클라이언트가 아직 만들어지지 않았을 때만 새로 생성 -> 싱글톤 패턴
                        # 앱 전체에서 클라이언트를 딱 한 번만 만들고 재사용
                        # API 연결을 매 요청마다 새로 여는 비용을 줄임
        _client = OpenAI(api_key=os.getenv('GMS_KEY'))
    return _client


def generate_embedding(keyword):
    response = _get_client().embeddings.create(
        model='text-embedding-3-small',
        input=keyword,
    )
    return response.data[0].embedding # keyword 벡터값 반환