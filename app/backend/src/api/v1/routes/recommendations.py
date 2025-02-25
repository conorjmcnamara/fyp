from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from src.services.recommendation import RecommendationService
from src.schemas.recommendation import RecommendationRequest, RecommendationResponse, PaperResponse
from src.core.database import get_db
from src.config.settings import TOP_K


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_recommendation_service(request: Request) -> RecommendationService:
    return request.app.state.recommendation_service


@router.post("", response_model=RecommendationResponse)
async def recommend_papers(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    recommended_papers = recommendation_service.recommend(
        db,
        request.title,
        request.abstract,
        TOP_K
    )
    return RecommendationResponse(papers=[PaperResponse(**paper) for paper in recommended_papers])
