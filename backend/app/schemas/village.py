from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VillageBase(BaseModel):
    village_code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=150)
    state: str = Field(min_length=2, max_length=100)
    district: str = Field(min_length=2, max_length=100)

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    elevation_m: float | None = Field(
        default=None,
        ge=-500,
        le=10000,
    )

    population: int | None = Field(
        default=None,
        ge=0,
    )

    has_health_facility: bool = False
    has_school: bool = False
    is_accessible: bool = True


class VillageCreate(VillageBase):
    risk_zone_public_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )


class VillageRead(VillageBase):
    model_config = ConfigDict(from_attributes=True)

    public_id: str
    risk_zone_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
