from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SensorReadingCreate(BaseModel):
    device_event_id: str = Field(
        min_length=8,
        max_length=64,
    )

    sensor_public_id: str = Field(
        min_length=36,
        max_length=36,
    )

    soil_moisture_percent: float | None = Field(
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

    tilt_degrees: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    vibration_level: float | None = Field(
        default=None,
        ge=0,
    )

    temperature_c: float | None = Field(
        default=None,
        ge=-60,
        le=80,
    )

    humidity_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    battery_level_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    signal_strength_dbm: float | None = Field(
        default=None,
        ge=-150,
        le=0,
    )

    recorded_at: datetime

    @model_validator(mode="after")
    def validate_reading(self):
        measurement_fields = (
            self.soil_moisture_percent,
            self.rainfall_mm,
            self.rainfall_rate_mm_hr,
            self.tilt_degrees,
            self.vibration_level,
            self.temperature_c,
            self.humidity_percent,
        )

        if all(value is None for value in measurement_fields):
            raise ValueError(
                "At least one sensor measurement must be provided."
            )

        if (
            self.recorded_at.tzinfo is None
            or self.recorded_at.utcoffset() is None
        ):
            raise ValueError(
                "recorded_at must include timezone information."
            )

        max_future_time = datetime.now(timezone.utc) + timedelta(
            minutes=5
        )

        if self.recorded_at > max_future_time:
            raise ValueError(
                "recorded_at cannot be more than 5 minutes in the future."
            )

        return self


class SensorReadingRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str
    device_event_id: str

    soil_moisture_percent: float | None = None
    rainfall_mm: float | None = None
    rainfall_rate_mm_hr: float | None = None
    tilt_degrees: float | None = None
    vibration_level: float | None = None
    temperature_c: float | None = None
    humidity_percent: float | None = None
    battery_level_percent: float | None = None
    signal_strength_dbm: float | None = None

    data_quality_status: str

    recorded_at: datetime
    received_at: datetime
