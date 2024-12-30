from fastapi import APIRouter
from src.api.v1.routes.messages import router as messages_router

router = APIRouter()
router.include_router(messages_router)
