from fastapi import APIRouter

router = APIRouter(prefix="/message", tags=["Messages"])


@router.get("/")
async def get_message():
    return {"message": "Hello"}
