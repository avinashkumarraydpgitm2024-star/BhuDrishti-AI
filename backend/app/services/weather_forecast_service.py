from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.weather_forecast import WeatherForecast
from backend.app.schemas.weather_forecast import WeatherForecastCreate

from datetime import datetime, timezone


def get_existing_forecast(
    db: Session,
    *,
    provider: str,
    latitude: float,
    longitude: float,
    forecast_for,
) -> WeatherForecast | None:
    statement = select(WeatherForecast).where(
        WeatherForecast.provider == provider,
        WeatherForecast.latitude == latitude,
        WeatherForecast.longitude == longitude,
        WeatherForecast.forecast_for == forecast_for,
    )

    return db.scalar(statement)


def create_weather_forecast(
    db: Session,
    forecast_data: WeatherForecastCreate,
) -> WeatherForecast:
    provider = forecast_data.provider.strip()

    existing = get_existing_forecast(
        db=db,
        provider=provider,
        latitude=forecast_data.latitude,
        longitude=forecast_data.longitude,
        forecast_for=forecast_data.forecast_for,
    )

    if existing is not None:
        existing.generated_at = forecast_data.generated_at
        existing.temperature_c = forecast_data.temperature_c
        existing.humidity_percent = forecast_data.humidity_percent
        existing.precipitation_mm = forecast_data.precipitation_mm
        existing.precipitation_probability_percent = (
            forecast_data.precipitation_probability_percent
        )
        existing.rain_mm = forecast_data.rain_mm
        existing.wind_speed_mps = forecast_data.wind_speed_mps
        existing.atmospheric_pressure_hpa = (
            forecast_data.atmospheric_pressure_hpa
        )

        try:
            db.commit()
            db.refresh(existing)
        except Exception:
            db.rollback()
            raise

        return existing

    forecast = WeatherForecast(
        provider=provider,
        latitude=forecast_data.latitude,
        longitude=forecast_data.longitude,
        forecast_for=forecast_data.forecast_for,
        generated_at=forecast_data.generated_at,
        temperature_c=forecast_data.temperature_c,
        humidity_percent=forecast_data.humidity_percent,
        precipitation_mm=forecast_data.precipitation_mm,
        precipitation_probability_percent=(
            forecast_data.precipitation_probability_percent
        ),
        rain_mm=forecast_data.rain_mm,
        wind_speed_mps=forecast_data.wind_speed_mps,
        atmospheric_pressure_hpa=(
            forecast_data.atmospheric_pressure_hpa
        ),
    )

    db.add(forecast)

    try:
        db.commit()
        db.refresh(forecast)
    except Exception:
        db.rollback()
        raise

    return forecast


def get_weather_forecasts(
    db: Session,
    *,
    latitude: float,
    longitude: float,
    limit: int = 168,
) -> list[WeatherForecast]:
    now = datetime.now(timezone.utc)

    statement = (
        select(WeatherForecast)
        .where(
            WeatherForecast.latitude == latitude,
            WeatherForecast.longitude == longitude,
            WeatherForecast.forecast_for >= now,
        )
        .order_by(
            WeatherForecast.forecast_for.asc()
        )
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )
    
def create_weather_forecasts(
    db: Session,
    forecast_items: list[WeatherForecastCreate],
) -> list[WeatherForecast]:
    saved_forecasts: list[WeatherForecast] = []

    for item in forecast_items:
        provider = item.provider.strip()

        existing = get_existing_forecast(
            db=db,
            provider=provider,
            latitude=item.latitude,
            longitude=item.longitude,
            forecast_for=item.forecast_for,
        )

        if existing is not None:
            existing.generated_at = item.generated_at
            existing.temperature_c = item.temperature_c
            existing.humidity_percent = item.humidity_percent
            existing.precipitation_mm = item.precipitation_mm
            existing.precipitation_probability_percent = (
                item.precipitation_probability_percent
            )
            existing.rain_mm = item.rain_mm
            existing.wind_speed_mps = item.wind_speed_mps
            existing.atmospheric_pressure_hpa = (
                item.atmospheric_pressure_hpa
            )

            saved_forecasts.append(existing)
            continue

        forecast = WeatherForecast(
            provider=provider,
            latitude=item.latitude,
            longitude=item.longitude,
            forecast_for=item.forecast_for,
            generated_at=item.generated_at,
            temperature_c=item.temperature_c,
            humidity_percent=item.humidity_percent,
            precipitation_mm=item.precipitation_mm,
            precipitation_probability_percent=(
                item.precipitation_probability_percent
            ),
            rain_mm=item.rain_mm,
            wind_speed_mps=item.wind_speed_mps,
            atmospheric_pressure_hpa=(
                item.atmospheric_pressure_hpa
            ),
        )

        db.add(forecast)
        saved_forecasts.append(forecast)

    try:
        db.commit()

        for forecast in saved_forecasts:
            db.refresh(forecast)

    except Exception:
        db.rollback()
        raise

    return saved_forecasts