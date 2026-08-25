import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base

from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "latitude",
            "longitude",
            "forecast_for",
            name="uq_weather_forecast_location_time",
        ),
    )

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

    provider: Mapped[str] = mapped_column(
        String(80),
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

    forecast_for: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    temperature_c: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    humidity_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    precipitation_mm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    precipitation_probability_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    rain_mm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    wind_speed_mps: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    atmospheric_pressure_hpa: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )