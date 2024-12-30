from fastapi import APIRouter

router = APIRouter(prefix="/message")

@router.get("/")
async def get_message():
    return {"message": "Hello"}