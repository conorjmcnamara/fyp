import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
from src.api import router as api_router
from src.api.v1.routes import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from src.services.factory import create_recommendation_service
    from src.services.pdf_processor import PdfProcessorService

    app.state.recommendation_service = create_recommendation_service()
    app.state.pdf_processor_service = PdfProcessorService()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(api_v1_router, prefix="/api/v1")
