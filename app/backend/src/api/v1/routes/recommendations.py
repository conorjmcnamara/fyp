from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from io import BytesIO
from src.services.recommendation import RecommendationService
from src.services.pdf_processor import PdfProcessorService
from src.schemas.recommendation import RecommendationRequest, RecommendationResponse, PaperResponse
from src.core.database import get_db
from src.config.settings import MAX_FILE_SIZE_BYTES

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_recommendation_service(request: Request) -> RecommendationService:
    return request.app.state.recommendation_service


def get_pdf_processor_service(request: Request) -> PdfProcessorService:
    return request.app.state.pdf_processor_service


@router.post("", response_model=RecommendationResponse)
async def recommend_from_text(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    try:
        recommended_papers = recommendation_service.recommend(
            db,
            request.title,
            request.abstract,
            request.numRecommendations
        )
        return RecommendationResponse(
            papers=[PaperResponse(**paper) for paper in recommended_papers]
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/upload", response_model=RecommendationResponse)
async def recommend_from_pdf(
    file: UploadFile = File(...),
    numRecommendations: int = Form(...),
    db: Session = Depends(get_db),
    pdf_processor_service: PdfProcessorService = Depends(get_pdf_processor_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=422, detail="Invalid file type. Please upload a PDF file.")
    
    if file.size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=422, detail=f"File size must not exceed the {MAX_FILE_SIZE_BYTES / 1024 / 1024} MB limit.")

    file_content = BytesIO(await file.read())
    title, abstract = pdf_processor_service.extract_title_and_abstract(file_content)
    if not title and not abstract:
        raise HTTPException(status_code=422, detail="Failed to parse a title and abstract.")

    try:
        RecommendationRequest(
            title=title,
            abstract=abstract,
            numRecommendations=numRecommendations
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {e}")

    try:
        recommended_papers = recommendation_service.recommend(
            db,
            title,
            abstract,
            numRecommendations
        )
        return RecommendationResponse(
            papers=[PaperResponse(**paper) for paper in recommended_papers]
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
