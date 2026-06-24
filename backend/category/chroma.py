import chromadb
# from .utils import generate_embedding

# 1. ChromaDB 클라이언트 (persistent - 파일로 저장됨)
#    : ChromaDB의 영구 저장 클라이언트를 생성
client = chromadb.PersistentClient(path="./chroma_db")

# 2. 컬렉션 4개 가져오기 (없으면 자동 생성)
jobs_col = client.get_or_create_collection(
    "jobs",
    metadata={"hnsw:space": "cosine"}
)
bootcamps_col = client.get_or_create_collection(
    "bootcamps",
    metadata={"hnsw:space": "cosine"}
)
certifications_col = client.get_or_create_collection(
    "certifications",
    metadata={"hnsw:space": "cosine"}
)
competitions_col = client.get_or_create_collection(
    "competitions",
    metadata={"hnsw:space": "cosine"}
)