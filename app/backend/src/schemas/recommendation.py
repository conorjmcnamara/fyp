from pydantic import BaseModel, validator
from typing import List
from src.config.settings import NUM_RECOMMENDATIONS_MIN, NUM_RECOMMENDATIONS_MAX


class RecommendationRequest(BaseModel):
    title: str
    abstract: str
    numRecommendations: int

    @validator("numRecommendations")
    def validate_num_recommendations(cls, v: int) -> int:
        if not (NUM_RECOMMENDATIONS_MIN <= v <= NUM_RECOMMENDATIONS_MAX):
            raise ValueError(
                f"numRecommendations must be between {NUM_RECOMMENDATIONS_MIN} and " +
                f"{NUM_RECOMMENDATIONS_MAX}"
            )
        return v


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
