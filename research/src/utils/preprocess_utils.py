from typing import List
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
