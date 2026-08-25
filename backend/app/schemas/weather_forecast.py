from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class WeatherForecastCreate(BaseModel):
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

    forecast_for: datetime
    generated_at: datetime

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

    precipitation_mm: float | None = Field(
        default=None,
        ge=0,
    )

    precipitation_probability_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    rain_mm: float | None = Field(
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

    @model_validator(mode="after")
    def validate_forecast_values(self):
        values = (
            self.temperature_c,
            self.humidity_percent,
            self.precipitation_mm,
            self.precipitation_probability_percent,
            self.rain_mm,
            self.wind_speed_mps,
            self.atmospheric_pressure_hpa,
        )

        if all(value is None for value in values):
            raise ValueError(
                "At least one forecast measurement must be provided."
            )

        return self


class WeatherForecastRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str
    provider: str

    latitude: float
    longitude: float

    forecast_for: datetime
    generated_at: datetime

    temperature_c: float | None = None
    humidity_percent: float | None = None
    precipitation_mm: float | None = None
    precipitation_probability_percent: float | None = None
    rain_mm: float | None = None
    wind_speed_mps: float | None = None
    atmospheric_pressure_hpa: float | None = None

    created_at: datetime