from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RiskZoneBase(BaseModel):
    zone_code: str = Field(
        min_length=2,
        max_length=50,
    )

    name: str = Field(
        min_length=2,
        max_length=150,
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

    elevation_m: float | None = Field(
        default=None,
        ge=-500,
        le=10000,
    )

    slope_degrees: float | None = Field(
        default=None,
        ge=0,
        le=90,
    )

    area_sq_km: float | None = Field(
        default=None,
        gt=0,
    )

    terrain_type: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    grid_resolution_m: int | None = Field(
        default=None,
        gt=0,
    )


class RiskZoneCreate(RiskZoneBase):
    pass


class RiskZoneRead(RiskZoneBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    