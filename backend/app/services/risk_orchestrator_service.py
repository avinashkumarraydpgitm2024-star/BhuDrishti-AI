from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.risk_zone import RiskZone
from backend.app.schemas.risk_assessment import RiskAssessmentCreate
from backend.app.services.alert_service import (
    create_alert_from_assessment,
)
from backend.app.services.risk_assessment_service import (
    create_risk_assessment,
)
from backend.app.services.risk_engine_service import (
    calculate_baseline_risk,
)
from backend.app.services.risk_fusion_service import (
    build_risk_engine_input,
    validate_risk_input_availability,
)


def run_risk_assessment(
    db: Session,
    *,
    risk_zone: RiskZone,
    forecast_horizon_minutes: int = 1440,
) -> RiskAssessment:
    if not risk_zone.is_active:
        raise ValueError(
            "Risk assessment cannot be generated for an inactive risk zone."
        )

    engine_input = build_risk_engine_input(
        db=db,
        risk_zone=risk_zone,
    )

    validate_risk_input_availability(
        engine_input
    )

    result = calculate_baseline_risk(
        engine_input
    )

    assessed_at = datetime.now(timezone.utc)

    valid_until = assessed_at + timedelta(
        minutes=forecast_horizon_minutes
    )

    assessment_data = RiskAssessmentCreate(
        risk_zone_public_id=risk_zone.public_id,
        severity=result.severity,
        risk_probability_percent=(
            result.risk_probability_percent
        ),
        confidence_percent=(
            result.confidence_percent
        ),
        forecast_horizon_minutes=(
            forecast_horizon_minutes
        ),
        model_name="bhudrishti-baseline-risk-engine",
        model_version="0.1.0",
        dominant_factor=result.dominant_factor,
        explanation=result.explanation,
        assessed_at=assessed_at,
        valid_until=valid_until,
    )

    assessment = create_risk_assessment(
        db=db,
        assessment_data=assessment_data,
    )

    create_alert_from_assessment(
        db=db,
        risk_zone=risk_zone,
        assessment=assessment,
    )

    return assessment
