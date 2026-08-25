import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class SatelliteObservation(Base):
    __tablename__ = "satellite_observations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    public_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    risk_zone_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "risk_zones.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        index=True,
    )

    satellite_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    scene_id: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        index=True,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        index=True,
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    cloud_cover_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ndvi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ndwi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    soil_moisture_index: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    surface_temperature_c: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    data_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    thumbnail_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )