from pydantic import BaseModel, model_validator
from typing import List
from src.config.settings import MAX_TEXT_LENGTH, NUM_RECOMMENDATIONS_MIN, NUM_RECOMMENDATIONS_MAX


class RecommendationRequest(BaseModel):
    title: str
    abstract: str
    numRecommendations: int

    @model_validator(mode="before")
    def validate_combined_length_and_num_recommendations(cls, values):
        title = values.get("title")
        abstract = values.get("abstract")
        numRecommendations = values.get("numRecommendations")

        if len(title) + len(abstract) > MAX_TEXT_LENGTH:
            # Prune the title and abstract
            remaining_len = MAX_TEXT_LENGTH - len(title)
            if remaining_len > 0:
                abstract = abstract[:remaining_len]
            else:
                title = title[:MAX_TEXT_LENGTH]
                abstract = ""
            
            values["title"] = title
            values["abstract"] = abstract

        if not (NUM_RECOMMENDATIONS_MIN <= numRecommendations <= NUM_RECOMMENDATIONS_MAX):
            raise ValueError(
                f"numRecommendations must be between {NUM_RECOMMENDATIONS_MIN} and " +
                f"{NUM_RECOMMENDATIONS_MAX}."
            )

        return values


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
