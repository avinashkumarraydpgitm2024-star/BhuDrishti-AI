from typing import Any

import httpx

from backend.app.core.config import settings

from datetime import datetime, timezone

from backend.app.schemas.weather_observation import WeatherObservationCreate

from backend.app.schemas.weather_forecast import WeatherForecastCreate

from backend.app.services.weather_forecast_service import (
    create_weather_forecasts,
)


class WeatherProviderError(Exception):
    """Raised when external weather data cannot be retrieved."""


def fetch_current_weather(
    *,
    latitude: float,
    longitude: float,
) -> dict[str, Any]:
    url = f"{settings.weather_api_base_url}/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "wind_speed_10m,"
            "surface_pressure"
        ),
        "timezone": "UTC",
    }

    try:
        response = httpx.get(
            url,
            params=params,
            timeout=10.0,
        )

        response.raise_for_status()

    except httpx.HTTPError as exc:
        raise WeatherProviderError(
            "Unable to retrieve weather data."
        ) from exc

    data = response.json()

    current = data.get("current")

    if not isinstance(current, dict):
        raise WeatherProviderError(
            "Weather provider returned an invalid response."
        )

    return current

def map_current_weather_to_observation(
    *,
    latitude: float,
    longitude: float,
    current: dict[str, Any],
) -> WeatherObservationCreate:
    observed_at_raw = current.get("time")

    if not isinstance(observed_at_raw, str):
        raise WeatherProviderError(
            "Weather provider response does not contain a valid time."
        )

    observed_at = datetime.fromisoformat(
        observed_at_raw
    ).replace(
        tzinfo=timezone.utc
    )

    return WeatherObservationCreate(
        provider="open-meteo",
        latitude=latitude,
        longitude=longitude,
        temperature_c=current.get("temperature_2m"),
        humidity_percent=current.get("relative_humidity_2m"),
        rainfall_mm=current.get("precipitation"),
        rainfall_rate_mm_hr=current.get("rain"),
        wind_speed_mps=current.get("wind_speed_10m"),
        atmospheric_pressure_hpa=current.get("surface_pressure"),
        observed_at=observed_at,
    )
from sqlalchemy.orm import Session

from backend.app.services.weather_service import create_weather_observation


def fetch_and_store_current_weather(
    *,
    db: Session,
    latitude: float,
    longitude: float,
):
    current = fetch_current_weather(
        latitude=latitude,
        longitude=longitude,
    )

    weather_data = map_current_weather_to_observation(
        latitude=latitude,
        longitude=longitude,
        current=current,
    )

    return create_weather_observation(
        db=db,
        weather_data=weather_data,
    )
def fetch_hourly_forecast(
    *,
    latitude: float,
    longitude: float,
    forecast_days: int = 7,
) -> dict[str, Any]:
    url = f"{settings.weather_api_base_url}/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "precipitation_probability,"
            "rain,"
            "wind_speed_10m,"
            "surface_pressure"
        ),
        "forecast_days": forecast_days,
        "timezone": "UTC",
    }

    try:
        response = httpx.get(
            url,
            params=params,
            timeout=15.0,
        )

        response.raise_for_status()

    except httpx.HTTPError as exc:
        raise WeatherProviderError(
            "Unable to retrieve weather forecast data."
        ) from exc

    data = response.json()

    hourly = data.get("hourly")

    if not isinstance(hourly, dict):
        raise WeatherProviderError(
            "Weather provider returned invalid forecast data."
        )

    return hourly

def map_hourly_forecast(
    *,
    latitude: float,
    longitude: float,
    hourly: dict[str, Any],
) -> list[WeatherForecastCreate]:
    times = hourly.get("time")

    if not isinstance(times, list):
        raise WeatherProviderError(
            "Weather forecast response does not contain valid timestamps."
        )

    generated_at = datetime.now(timezone.utc)
    forecasts: list[WeatherForecastCreate] = []

    fields = {
        "temperature_2m": hourly.get("temperature_2m"),
        "relative_humidity_2m": hourly.get("relative_humidity_2m"),
        "precipitation": hourly.get("precipitation"),
        "precipitation_probability": hourly.get(
            "precipitation_probability"
        ),
        "rain": hourly.get("rain"),
        "wind_speed_10m": hourly.get("wind_speed_10m"),
        "surface_pressure": hourly.get("surface_pressure"),
    }

    for field_name, values in fields.items():
        if not isinstance(values, list) or len(values) != len(times):
            raise WeatherProviderError(
                f"Invalid hourly forecast field: {field_name}."
            )

    for index, forecast_time in enumerate(times):
        if not isinstance(forecast_time, str):
            raise WeatherProviderError(
                "Weather forecast contains an invalid timestamp."
            )

        forecast_for = datetime.fromisoformat(
            forecast_time
        ).replace(
            tzinfo=timezone.utc
        )

        forecasts.append(
            WeatherForecastCreate(
                provider="open-meteo",
                latitude=latitude,
                longitude=longitude,
                forecast_for=forecast_for,
                generated_at=generated_at,
                temperature_c=fields["temperature_2m"][index],
                humidity_percent=fields[
                    "relative_humidity_2m"
                ][index],
                precipitation_mm=fields["precipitation"][index],
                precipitation_probability_percent=fields[
                    "precipitation_probability"
                ][index],
                rain_mm=fields["rain"][index],
                wind_speed_mps=fields["wind_speed_10m"][index],
                atmospheric_pressure_hpa=fields[
                    "surface_pressure"
                ][index],
            )
        )

    return forecasts

def fetch_map_and_store_hourly_forecast(
    *,
    db: Session,
    latitude: float,
    longitude: float,
    forecast_days: int = 7,
):
    hourly = fetch_hourly_forecast(
        latitude=latitude,
        longitude=longitude,
        forecast_days=forecast_days,
    )

    forecast_items = map_hourly_forecast(
        latitude=latitude,
        longitude=longitude,
        hourly=hourly,
    )

    return create_weather_forecasts(
        db=db,
        forecast_items=forecast_items,
    )
