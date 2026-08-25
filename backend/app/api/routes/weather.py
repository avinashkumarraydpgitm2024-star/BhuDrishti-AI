from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.weather_observation import (
    WeatherObservationCreate,
    WeatherObservationRead,
)
from backend.app.services.weather_service import (
    create_weather_observation,
    get_latest_weather_observation,
)

from backend.app.services.weather_provider_service import (
    WeatherProviderError,
    fetch_and_store_current_weather,
    fetch_map_and_store_hourly_forecast,
)
from backend.app.schemas.weather_forecast import WeatherForecastRead

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)
@router.post(
    "/observations",
    response_model=WeatherObservationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_observation(
    weather_data: WeatherObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> WeatherObservationRead:
    observation = create_weather_observation(
        db=db,
        weather_data=weather_data,
    )

    return WeatherObservationRead.model_validate(
        observation
    )
@router.get(
    "/observations/latest",
    response_model=WeatherObservationRead,
)
def get_latest_observation(
    latitude: float = Query(
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ge=-180,
        le=180,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> WeatherObservationRead:
    observation = get_latest_weather_observation(
        db=db,
        latitude=latitude,
        longitude=longitude,
    )

    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather observation not found.",
        )

    return WeatherObservationRead.model_validate(
        observation
    )

@router.post(
    "/sync-current",
    response_model=WeatherObservationRead,
    status_code=status.HTTP_201_CREATED,
)
def sync_current_weather(
    latitude: float = Query(
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ge=-180,
        le=180,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> WeatherObservationRead:
    try:
        observation = fetch_and_store_current_weather(
            db=db,
            latitude=latitude,
            longitude=longitude,
        )
    except WeatherProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return WeatherObservationRead.model_validate(
        observation
    )

@router.post(
    "/sync-forecast",
    response_model=list[WeatherForecastRead],
    status_code=status.HTTP_201_CREATED,
)
def sync_weather_forecast(
    latitude: float = Query(
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ge=-180,
        le=180,
    ),
    forecast_days: int = Query(
        default=7,
        ge=1,
        le=7,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> list[WeatherForecastRead]:
    try:
        forecasts = fetch_map_and_store_hourly_forecast(
            db=db,
            latitude=latitude,
            longitude=longitude,
            forecast_days=forecast_days,
        )
    except WeatherProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return [
        WeatherForecastRead.model_validate(forecast)
        for forecast in forecasts
    ]
from backend.app.services.weather_forecast_service import (
    get_weather_forecasts,
)


@router.get(
    "/forecast",
    response_model=list[WeatherForecastRead],
)
def get_forecast(
    latitude: float = Query(
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ge=-180,
        le=180,
    ),
    limit: int = Query(
        default=168,
        ge=1,
        le=336,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> list[WeatherForecastRead]:
    forecasts = get_weather_forecasts(
        db=db,
        latitude=latitude,
        longitude=longitude,
        limit=limit,
    )

    return [
        WeatherForecastRead.model_validate(forecast)
        for forecast in forecasts
    ]