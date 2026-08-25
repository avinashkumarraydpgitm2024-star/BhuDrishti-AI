from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.risk_assessment import RiskSeverity


class RiskAssessmentCreate(BaseModel):
    risk_zone_public_id: str = Field(
        min_length=36,
        max_length=36,
    )

    severity: RiskSeverity

    risk_probability_percent: float = Field(
        ge=0,
        le=100,
    )

    confidence_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    forecast_horizon_minutes: int = Field(
        ge=0,
        le=10080,
    )

    model_name: str = Field(
        default="bhudrishti-risk-engine",
        min_length=2,
        max_length=120,
    )

    model_version: str = Field(
        default="0.1.0",
        min_length=1,
        max_length=50,
    )

    dominant_factor: str | None = Field(
        default=None,
        max_length=150,
    )

    explanation: str | None = Field(
        default=None,
        max_length=3000,
    )

    assessed_at: datetime

    valid_until: datetime | None = None


class RiskAssessmentRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: str

    severity: RiskSeverity

    risk_probability_percent: float

    confidence_percent: float | None

    forecast_horizon_minutes: int

    model_name: str

    model_version: str

    dominant_factor: str | None

    explanation: str | None

    assessed_at: datetime

    valid_until: datetime | None

    created_at: datetime