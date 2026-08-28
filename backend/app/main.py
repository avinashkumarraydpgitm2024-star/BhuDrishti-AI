from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.api.v1 import router as api_v1_router


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-Powered Real-Time Geo-Hazard Intelligence "
        "and Early Warning Platform for North-East India"
    ),
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_v1_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
async def root():
    return {
        "platform": settings.app_name,
        "status": "operational",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "bhudrishti-backend",
        "environment": settings.environment,
    }
