from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.models.weather_forecast import WeatherForecast
from backend.app.services.risk_engine_service import RiskEngineInput
from backend.app.services.risk_input_service import (
    aggregate_zone_sensor_inputs,
)

from backend.app.services.historical_risk_service import (
    calculate_historical_risk_score,
)


def get_future_weather_for_zone(
    db: Session,
    *,
    risk_zone: RiskZone,
    hours: int = 24,
) -> list[WeatherForecast]:
    now = datetime.now(timezone.utc)
    end_time = now + timedelta(hours=hours)

    statement = (
        select(WeatherForecast)
        .where(
            WeatherForecast.latitude == risk_zone.latitude,
            WeatherForecast.longitude == risk_zone.longitude,
            WeatherForecast.forecast_for >= now,
            WeatherForecast.forecast_for <= end_time,
        )
        .order_by(
            WeatherForecast.forecast_for.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def _sum_values(
    values: list[float],
) -> float | None:
    if not values:
        return None

    return sum(values)


def _maximum(
    values: list[float],
) -> float | None:
    if not values:
        return None

    return max(values)


def build_risk_engine_input(
    db: Session,
    *,
    risk_zone: RiskZone,
) -> RiskEngineInput:
    sensor_data = aggregate_zone_sensor_inputs(
        db=db,
        risk_zone_id=risk_zone.id,
    )
    historical_risk_score = calculate_historical_risk_score(
        db=db,
        risk_zone_id=risk_zone.id,
    )

    
    satellite_observation = get_latest_satellite_observation_for_zone(
        db=db,
        risk_zone_id=risk_zone.id,
    )
    forecasts = get_future_weather_for_zone(
        db=db,
        risk_zone=risk_zone,
        hours=24,
    )

    precipitation_values = [
        forecast.precipitation_mm
        for forecast in forecasts
        if forecast.precipitation_mm is not None
    ]

    precipitation_probability_values = [
        forecast.precipitation_probability_percent
        for forecast in forecasts
        if forecast.precipitation_probability_percent is not None
    ]

    rainfall_24h_mm = _sum_values(
        precipitation_values
    )

    max_precipitation_probability = _maximum(
        precipitation_probability_values
    )

    return RiskEngineInput(
        rainfall_rate_mm_hr=(
            sensor_data["rainfall_rate_mm_hr"]
        ),
        rainfall_24h_mm=rainfall_24h_mm,
        soil_moisture_percent=(
            sensor_data["soil_moisture_percent"]
        ),
        slope_degrees=risk_zone.slope_degrees,
        vibration_level=(
            sensor_data["vibration_level"]
        ),
        tilt_degrees=(
            sensor_data["tilt_degrees"]
        ),
        precipitation_probability_percent=(
            max_precipitation_probability
        ),
        historical_risk_score=historical_risk_score,
    
        satellite_ndwi=(
            satellite_observation.ndwi
            if satellite_observation is not None
            else None
        ),
        satellite_soil_moisture_index=(
            satellite_observation.soil_moisture_index
            if satellite_observation is not None
            else None
        ),
        satellite_ndvi=(
            satellite_observation.ndvi
            if satellite_observation is not None
            else None
        ),
    )
def validate_risk_input_availability(
    risk_input: RiskEngineInput,
) -> None:
    important_inputs = [
        risk_input.rainfall_rate_mm_hr,
        risk_input.rainfall_24h_mm,
        risk_input.soil_moisture_percent,
        risk_input.slope_degrees,
        risk_input.precipitation_probability_percent,
    ]

    available_count = sum(
        value is not None
        for value in important_inputs
    )

    if available_count < 2:
        raise ValueError(
            "Insufficient data to generate a reliable risk assessment."
        )




