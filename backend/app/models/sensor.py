import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class SensorType(str, enum.Enum):
    SOIL_MOISTURE = "soil_moisture"
    RAIN_GAUGE = "rain_gauge"
    TILT = "tilt"
    VIBRATION = "vibration"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    MULTI_SENSOR = "multi_sensor"


class SensorStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    FAULTY = "faulty"
    OFFLINE = "offline"


class Sensor(Base):
    __tablename__ = "sensors"

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

    sensor_code: Mapped[str] = mapped_column(
        String(60),
        unique=True,
        nullable=False,
        index=True,
    )

    device_api_key_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    sensor_type: Mapped[SensorType] = mapped_column(
        Enum(
            SensorType,
            name="sensor_type",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[SensorStatus] = mapped_column(
        Enum(
            SensorStatus,
            name="sensor_status",
        ),
        nullable=False,
        default=SensorStatus.ACTIVE,
        index=True,
    )

    risk_zone_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "risk_zones.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    elevation_m: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    installation_depth_cm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    firmware_version: Mapped[str | None] = mapped_column(
        String(80),
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

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    installed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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

