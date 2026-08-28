import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

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

    device_event_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sensors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    soil_moisture_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    rainfall_mm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    rainfall_rate_mm_hr: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    tilt_degrees: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    vibration_level: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    temperature_c: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    humidity_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    battery_level_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    signal_strength_dbm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    data_quality_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="valid",
        index=True,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
