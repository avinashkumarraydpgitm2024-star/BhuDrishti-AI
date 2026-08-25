from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class WeatherObservationCreate(BaseModel):
    provider: str = Field(
        min_length=2,
        max_length=80,
    )

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    temperature_c: float | None = Field(
        default=None,
        ge=-80,
        le=60,
    )

    humidity_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    rainfall_mm: float | None = Field(
        default=None,
        ge=0,
    )

    rainfall_rate_mm_hr: float | None = Field(
        default=None,
        ge=0,
    )

    wind_speed_mps: float | None = Field(
        default=None,
        ge=0,
    )

    atmospheric_pressure_hpa: float | None = Field(
        default=None,
        ge=800,
        le=1100,
    )

    observed_at: datetime

    @model_validator(mode="after")
    def validate_weather_values(self):
        values = (
            self.temperature_c,
            self.humidity_percent,
            self.rainfall_mm,
            self.rainfall_rate_mm_hr,
            self.wind_speed_mps,
            self.atmospheric_pressure_hpa,
        )

        if all(value is None for value in values):
            raise ValueError(
                "At least one weather measurement must be provided."
            )

        return self


class WeatherObservationRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str
    provider: str
    latitude: float
    longitude: float

    temperature_c: float | None = None
    humidity_percent: float | None = None
    rainfall_mm: float | None = None
    rainfall_rate_mm_hr: float | None = None
    wind_speed_mps: float | None = None
    atmospheric_pressure_hpa: float | None = None

    observed_at: datetime
    received_at: datetime