from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routes import router as api_v1_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")


if __name__ == "__main__":
    import os
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    port = int(os.getenv("BACKEND_PORT"))
    uvicorn.run(app, host="0.0.0.0", port=port)
