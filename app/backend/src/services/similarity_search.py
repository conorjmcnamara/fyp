import numpy as np
from typing import List, Tuple
from src.utils.file_utils import read_embeddings, read_obj


class SimilaritySearchService:
    def __init__(self, index_path: str, ids_path: str):
        self.index = read_embeddings(index_path)
        self.ids: List[str] = read_obj(ids_path)

    def search(self, query_embedding: np.ndarray, top_k: int) -> Tuple[List[str], List[float]]:
        distances, indices = self.index.search(query_embedding, top_k)
        ids = [self.ids[idx] for idx in indices[0]]
        scores = [1 - dist for dist in distances[0]]
        return ids, scores
