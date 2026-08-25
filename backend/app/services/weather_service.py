from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.weather_observation import WeatherObservation
from backend.app.schemas.weather_observation import WeatherObservationCreate


def create_weather_observation(
    db: Session,
    weather_data: WeatherObservationCreate,
) -> WeatherObservation:
    observation = WeatherObservation(
        provider=weather_data.provider.strip(),
        latitude=weather_data.latitude,
        longitude=weather_data.longitude,
        temperature_c=weather_data.temperature_c,
        humidity_percent=weather_data.humidity_percent,
        rainfall_mm=weather_data.rainfall_mm,
        rainfall_rate_mm_hr=weather_data.rainfall_rate_mm_hr,
        wind_speed_mps=weather_data.wind_speed_mps,
        atmospheric_pressure_hpa=weather_data.atmospheric_pressure_hpa,
        observed_at=weather_data.observed_at,
    )

    db.add(observation)

    try:
        db.commit()
        db.refresh(observation)
    except Exception:
        db.rollback()
        raise

    return observation


def get_latest_weather_observation(
    db: Session,
    *,
    latitude: float,
    longitude: float,
) -> WeatherObservation | None:
    statement = (
        select(WeatherObservation)
        .where(
            WeatherObservation.latitude == latitude,
            WeatherObservation.longitude == longitude,
        )
        .order_by(
            WeatherObservation.observed_at.desc()
        )
        .limit(1)
    )

    return db.scalar(statement)