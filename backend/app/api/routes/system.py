from fastapi import APIRouter

from backend.app.core.config import settings


router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/status")
async def system_status():
    return {
        "platform": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "operational",
    }


@router.get("/health")
async def system_health():
    return {
        "status": "healthy",
        "service": "bhudrishti-backend",
        "environment": settings.environment,
    }