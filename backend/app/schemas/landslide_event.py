from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.landslide_event import LandslideSeverity


class LandslideEventCreate(BaseModel):
    risk_zone_public_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )

    event_code: str = Field(
        min_length=2,
        max_length=60,
    )

    state: str = Field(
        min_length=2,
        max_length=100,
    )

    district: str = Field(
        min_length=2,
        max_length=100,
    )

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    occurred_at: datetime

    severity: LandslideSeverity

    rainfall_24h_mm: float | None = Field(
        default=None,
        ge=0,
    )

    soil_moisture_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    slope_degrees: float | None = Field(
        default=None,
        ge=0,
        le=90,
    )

    fatalities: int | None = Field(
        default=None,
        ge=0,
    )

    injuries: int | None = Field(
        default=None,
        ge=0,
    )

    affected_area_sq_km: float | None = Field(
        default=None,
        ge=0,
    )

    road_blocked: bool = False

    source: str | None = Field(
        default=None,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=3000,
    )


class LandslideEventRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str
    event_code: str

    state: str
    district: str

    latitude: float
    longitude: float

    occurred_at: datetime
    severity: LandslideSeverity

    rainfall_24h_mm: float | None
    soil_moisture_percent: float | None
    slope_degrees: float | None

    fatalities: int | None
    injuries: int | None
    affected_area_sq_km: float | None

    road_blocked: bool

    source: str | None
    description: str | None

    created_at: datetime