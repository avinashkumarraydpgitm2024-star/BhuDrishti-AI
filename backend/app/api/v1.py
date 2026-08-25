from fastapi import APIRouter

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.landslide_events import (
    router as landslide_events_router,
)
from backend.app.api.routes.protected import router as protected_router
from backend.app.api.routes.risk_assessments import (
    router as risk_assessments_router,
)
from backend.app.api.routes.risk_zones import router as risk_zones_router
from backend.app.api.routes.satellite_observations import (
    router as satellite_observations_router,
)
from backend.app.api.routes.sensor_readings import (
    router as sensor_readings_router,
)
from backend.app.api.routes.sensors import router as sensors_router
from backend.app.api.routes.system import router as system_router
from backend.app.api.routes.weather import router as weather_router


router = APIRouter()


router.include_router(system_router)
router.include_router(auth_router)
router.include_router(protected_router)
router.include_router(risk_zones_router)
router.include_router(sensors_router)
router.include_router(sensor_readings_router)
router.include_router(weather_router)
router.include_router(risk_assessments_router)
router.include_router(landslide_events_router)
router.include_router(satellite_observations_router)