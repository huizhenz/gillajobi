from rest_framework.decorators import api_view
from rest_framework.response import Response

from category.chroma import jobs_col, bootcamps_col, certifications_col, competitions_col
from category.utils import generate_embedding

@api_view(['POST'])
def search(request):
    keyword = request.data.get('keyword')
    
    # 사용자가 검색한 키워드 임베딩
    embedding = generate_embedding(keyword)
    
    # 1. collection.query() → 각 컬렉션별로 변수에 담기
    jobs_result = jobs_col.query(query_embeddings=[embedding], n_results=3)
    bootcamps_result = bootcamps_col.query(query_embeddings=[embedding], n_results=3)
    certifications_result = certifications_col.query(query_embeddings=[embedding], n_results=3)
    competitions_result = competitions_col.query(query_embeddings=[embedding], n_results=3)
    
    # 2. Response에 컬렉션 객체가 아닌 결과의 메타데이터 넣기
    return Response({
        "jobs": jobs_result['metadatas'][0],
        "bootcamps": bootcamps_result['metadatas'][0],
        "certifications": certifications_result['metadatas'][0],
        "competitions": competitions_result['metadatas'][0],
    })