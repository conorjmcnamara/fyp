from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Dict, Any
from src.services.embedding import EmbeddingService
from src.services.similarity_search import SimilaritySearchService
from src.crud.paper import get_papers_by_ids


class RecommendationService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        search_service: SimilaritySearchService
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
        ids, similarity_scores = self.search_service.search(query_embedding, top_k)
        similarity_scores_map = {UUID(id): score for id, score in zip(ids, similarity_scores)}
        papers = get_papers_by_ids(db, [UUID(id) for id in ids])

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
                "similarity_score": similarity_scores_map[paper.id]
            }
            for paper in papers
        ]
