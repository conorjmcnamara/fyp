from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}
