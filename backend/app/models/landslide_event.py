import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class LandslideSeverity(str, enum.Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    SEVERE = "severe"


class LandslideEvent(Base):
    __tablename__ = "landslide_events"

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

    event_code: Mapped[str] = mapped_column(
        String(60),
        unique=True,
        nullable=False,
        index=True,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    district: Mapped[str] = mapped_column(
        String(100),
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

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    severity: Mapped[LandslideSeverity] = mapped_column(
        Enum(
            LandslideSeverity,
            name="landslide_severity",
        ),
        nullable=False,
        index=True,
    )

    rainfall_24h_mm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    soil_moisture_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    slope_degrees: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    fatalities: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    injuries: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    affected_area_sq_km: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    road_blocked: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    source: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    