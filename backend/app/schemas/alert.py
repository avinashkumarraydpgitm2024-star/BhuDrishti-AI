from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.risk_assessment import RiskSeverity


class AlertCreate(BaseModel):
    risk_zone_public_id: str = Field(
        min_length=36,
        max_length=36,
    )

    risk_assessment_public_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )

    severity: RiskSeverity

    title: str = Field(
        min_length=3,
        max_length=180,
    )

    message: str = Field(
        min_length=3,
        max_length=3000,
    )

    audience: str = Field(
        default="authority",
        min_length=2,
        max_length=100,
    )


class AlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: str
    severity: RiskSeverity
    title: str
    message: str
    audience: str
    status: str

    risk_zone_id: int
    risk_assessment_id: int | None

    created_at: datetime
    acknowledged_at: datetime | None
    resolved_at: datetime | None
