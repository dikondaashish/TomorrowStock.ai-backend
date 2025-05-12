from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings

def create_application() -> FastAPI:
    application = FastAPI(
        title="Stock Predictor API",
        description="API for stock price prediction",
        version="0.1.0"
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development; restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router)

    @application.get("/")
    async def root():
        return {"message": "Welcome to the Stock Predictor API"}

    return application

app = create_application() 