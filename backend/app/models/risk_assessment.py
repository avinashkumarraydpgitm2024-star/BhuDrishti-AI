import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class RiskSeverity(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

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

    risk_zone_id: Mapped[int] = mapped_column(
        ForeignKey(
            "risk_zones.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    severity: Mapped[RiskSeverity] = mapped_column(
        Enum(
            RiskSeverity,
            name="risk_severity",
        ),
        nullable=False,
        index=True,
    )

    risk_probability_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    forecast_horizon_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        index=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="bhudrishti-risk-engine",
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="0.1.0",
    )

    dominant_factor: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    valid_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )