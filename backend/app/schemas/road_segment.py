from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoadSegmentBase(BaseModel):
    road_code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=150)
    road_type: str = Field(min_length=2, max_length=50)

    state: str = Field(min_length=2, max_length=100)
    district: str = Field(min_length=2, max_length=100)

    start_latitude: float = Field(ge=-90, le=90)
    start_longitude: float = Field(ge=-180, le=180)
    end_latitude: float = Field(ge=-90, le=90)
    end_longitude: float = Field(ge=-180, le=180)

    length_km: float | None = Field(
        default=None,
        ge=0,
    )

    is_blocked: bool = False

    blockage_reason: str | None = Field(
        default=None,
        max_length=250,
    )


class RoadSegmentCreate(RoadSegmentBase):
    risk_zone_public_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )


class RoadSegmentRead(RoadSegmentBase):
    model_config = ConfigDict(from_attributes=True)

    public_id: str
    risk_zone_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
