import numpy as np
import faiss
from typing import List, Tuple
from src.utils.file_utils import read_embeddings, read_obj


class IndexSearchService:
    def __init__(self, index_path: str, ids_path: str):
        raise Exception()
        self.index = read_embeddings(index_path)
        self.ids: List[str] = read_obj(ids_path)

    def search(self, query_embedding: np.ndarray, top_k: int) -> Tuple[List[str], List[float]]:
        query_embedding = query_embedding.astype(np.float32)
        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, top_k)
        ids = [self.ids[idx] for idx in indices[0]]
        scores = [dist for dist in distances[0]]
        return ids, scores
