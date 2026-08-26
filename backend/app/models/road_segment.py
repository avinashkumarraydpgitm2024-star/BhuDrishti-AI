import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class RoadSegment(Base):
    __tablename__ = "road_segments"

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

    road_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    road_type: Mapped[str] = mapped_column(
        String(50),
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

    start_latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    start_longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    end_latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    end_longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    length_km: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    risk_zone_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "risk_zones.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    blockage_reason: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
