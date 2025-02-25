from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):
    title: str
    abstract: str


class AuthorResponse(BaseModel):
    first_name: str
    last_name: str


class PaperResponse(BaseModel):
    id: str
    title: str
    year: int
    abstract: str
    venue: str
    authors: List[AuthorResponse]
    recommendation_score: float


class RecommendationResponse(BaseModel):
    papers: List[PaperResponse]
