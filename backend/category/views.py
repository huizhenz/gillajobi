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
    filtered_jobs = [
        meta for meta, dist in zip(jobs_result['metadatas'][0], jobs_result['distances'][0])
        # if dist < 1.2
    ]
    print("jobs distances:", jobs_result['distances'])  # ← 여기

    bootcamps_result = bootcamps_col.query(query_embeddings=[embedding], n_results=3)
    filtered_bootcamps = [
        meta for meta, dist in zip(bootcamps_result['metadatas'][0], bootcamps_result['distances'][0])
        # if dist < 1.2
    ]

    certifications_result = certifications_col.query(query_embeddings=[embedding], n_results=3)
    filtered_certifications = [
        meta for meta, dist in zip(certifications_result['metadatas'][0], certifications_result['distances'][0])
        # if dist < 1.2
    ]

    competitions_result = competitions_col.query(query_embeddings=[embedding], n_results=3)
    filtered_competitions = [
        meta for meta, dist in zip(competitions_result['metadatas'][0], competitions_result['distances'][0])
        # if dist < 1.2
    ]
    
    # 2. Response에 컬렉션 객체가 아닌 결과의 메타데이터 넣기
    return Response({
        "jobs": filtered_jobs,
        "bootcamps": filtered_bootcamps,
        "certifications": filtered_certifications,
        "competitions": filtered_competitions,
    })