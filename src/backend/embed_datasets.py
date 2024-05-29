import sys
sys.path.append('')
from src.backend.embeddings.embedding import Embedding
from src.backend.embeddings.vector_db import Vector_DB

class DatasetEmbedding:
    def __init__(self) -> None:
        v = Vector_DB()
        self.db = v.retrieve(Embedding().openai(), collection='search')

    def add_text(self, text: str, metadata: dict):
        self.db.add_texts([text], metadatas=[metadata])

    def get_similar(self, text: str, k: int = 4):
        return self.db.similarity_search_with_score(text, k=k)