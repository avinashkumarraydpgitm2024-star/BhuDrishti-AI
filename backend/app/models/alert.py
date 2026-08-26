import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base
from backend.app.models.risk_assessment import RiskSeverity


class AlertStatus(str):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class Alert(Base):
    __tablename__ = "alerts"

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

    risk_assessment_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "risk_assessments.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    severity: Mapped[RiskSeverity] = mapped_column(
        Enum(RiskSeverity),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    audience: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="authority",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=AlertStatus.ACTIVE,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
