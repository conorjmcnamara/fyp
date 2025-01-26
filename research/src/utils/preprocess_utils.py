import faiss
import numpy as np
from typing import List, Tuple
from src.data_models.paper import Paper


def remove_missing_references(papers: List[Paper]) -> None:
    ids = set(paper.id for paper in papers)
    for paper in papers:
        paper.references = [ref_id for ref_id in paper.references if ref_id in ids]


def compute_citation_counts(papers: List[Paper]) -> None:
    for paper in papers:
        paper.citation_count = 0

    paper_map = {paper.id: paper for paper in papers}
    for paper in papers:
        for ref_id in paper.references:
            if ref_id in paper_map:
                paper_map[ref_id].citation_count += 1


def extract_embeddings_from_index(index: faiss.Index) -> np.ndarray:
    embeddings = np.zeros((index.ntotal, index.d), dtype=np.float32)
    for i in range(index.ntotal):
        index.reconstruct(i, embeddings[i])
    return embeddings


def align_embeddings(
    aligned_ids: List[str],
    to_align_embeddings: np.ndarray,
    to_align_ids: List[str]
) -> Tuple[np.ndarray, List[str]]:
    if sorted(aligned_ids) != sorted(to_align_ids):
        raise ValueError("IDs in 'aligned_ids' and 'to_align_ids' do not match.")

    to_align_id_to_idx = {to_align_ids[i]: i for i in range(len(to_align_ids))}
    aligned_b = np.array([to_align_embeddings[to_align_id_to_idx[id]] for id in aligned_ids])
    return aligned_b, aligned_ids
