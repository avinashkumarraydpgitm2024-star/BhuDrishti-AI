from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.sensor import (
    SensorStatus,
    SensorType,
)


class SensorBase(BaseModel):
    sensor_code: str = Field(
        min_length=2,
        max_length=60,
    )

    name: str = Field(
        min_length=2,
        max_length=150,
    )

    sensor_type: SensorType

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    elevation_m: float | None = Field(
        default=None,
        ge=-500,
        le=10000,
    )

    installation_depth_cm: float | None = Field(
        default=None,
        ge=0,
    )

    firmware_version: str | None = Field(
        default=None,
        max_length=80,
    )


class SensorCreate(SensorBase):
    risk_zone_public_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )


class SensorRead(SensorBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str

    status: SensorStatus

    battery_level_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    signal_strength_dbm: float | None = None

    last_seen_at: datetime | None = None

    installed_at: datetime | None = None

    created_at: datetime

    updated_at: datetime
        
class SensorProvisionRead(SensorRead):
    device_api_key: str = Field(
        min_length=32,
        max_length=128,
    )
