from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class SatelliteObservationCreate(BaseModel):
    risk_zone_public_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )

    provider: str = Field(
        min_length=2,
        max_length=80,
    )

    satellite_name: str | None = Field(
        default=None,
        max_length=100,
    )

    scene_id: str = Field(
        min_length=2,
        max_length=150,
    )

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    captured_at: datetime

    cloud_cover_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ndvi: float | None = Field(
        default=None,
        ge=-1,
        le=1,
    )

    ndwi: float | None = Field(
        default=None,
        ge=-1,
        le=1,
    )

    soil_moisture_index: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    surface_temperature_c: float | None = Field(
        default=None,
        ge=-100,
        le=100,
    )

    data_url: HttpUrl | None = None
    thumbnail_url: HttpUrl | None = None

    @model_validator(mode="after")
    def validate_observation_values(self):
        values = (
            self.ndvi,
            self.ndwi,
            self.soil_moisture_index,
            self.surface_temperature_c,
        )

        if all(value is None for value in values):
            raise ValueError(
                "At least one satellite-derived measurement must be provided."
            )

        return self


class SatelliteObservationRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str
    provider: str
    satellite_name: str | None
    scene_id: str

    latitude: float
    longitude: float

    captured_at: datetime

    cloud_cover_percent: float | None

    ndvi: float | None
    ndwi: float | None
    soil_moisture_index: float | None
    surface_temperature_c: float | None

    data_url: str | None
    thumbnail_url: str | None

    created_at: datetime