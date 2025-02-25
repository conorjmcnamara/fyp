from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Dict, Any
from src.services.embedding import EmbeddingService
from src.services.index_search import IndexSearchService
from src.crud.paper import get_papers_by_ids


class RecommendationService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        search_service: IndexSearchService
    ):
        self.embedding_service = embedding_service
        self.search_service = search_service

    def recommend(
        self,
        db: Session,
        title: str,
        abstract: str,
        top_k: int
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_service.embed(title, abstract)
        ids, scores = self.search_service.search(query_embedding, top_k)
        ids = [UUID(id) for id in ids]
        scores_map = {id: score for id, score in zip(ids, scores)}

        papers = get_papers_by_ids(db, [id for id in ids])
        papers_map = {paper.id: paper for paper in papers}

        return [
            {
                "id": str(paper.id),
                "title": paper.title,
                "year": paper.year,
                "abstract": paper.abstract,
                "venue": paper.venue.name,
                "authors": [
                    {"first_name": author.first_name, "last_name": author.last_name}
                    for author in paper.authors
                ],
                "recommendation_score": round(scores_map[paper.id], 4)
            }
            for id in ids
            if (paper := papers_map.get(id)) is not None
        ]
