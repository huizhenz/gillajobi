import chromadb

_client = None

def _get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path="chroma_data")
    return _client

def get_collection(name):
    """앱별로 컬렉션만 분리해서 사용"""
    return _get_chroma_client().get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )