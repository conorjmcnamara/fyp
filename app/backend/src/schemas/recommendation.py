from pydantic import BaseModel, model_validator
from typing import List
from src.config.settings import NUM_RECOMMENDATIONS_MIN, NUM_RECOMMENDATIONS_MAX


class RecommendationRequest(BaseModel):
    title: str
    abstract: str
    numRecommendations: int

    @model_validator(mode="before")
    def validate_combined_length_and_num_recommendations(cls, values):
        title = values.get("title")
        abstract = values.get("abstract")
        numRecommendations = values.get("numRecommendations")

        # Validate the combined length of title and abstract
        if len(title) + len(abstract) > 1500:
            remaining_len = 1500 - len(title)
            if remaining_len > 0:
                abstract = abstract[:remaining_len]
            else:
                title = title[:1500]
                abstract = ""
            
            values["title"] = title
            values["abstract"] = abstract

        # Validate the numRecommendations range
        if not (NUM_RECOMMENDATIONS_MIN <= numRecommendations <= NUM_RECOMMENDATIONS_MAX):
            raise ValueError(f"numRecommendations must be between {NUM_RECOMMENDATIONS_MIN} and {NUM_RECOMMENDATIONS_MAX}.")

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
