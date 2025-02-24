from fastapi import APIRouter
from src.api.v1.routes.recommendations import router as recommendations_router

router = APIRouter()
router.include_router(recommendations_router)
