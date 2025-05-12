from fastapi import APIRouter
from app.api.endpoints import health, prediction, auth

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"]) 