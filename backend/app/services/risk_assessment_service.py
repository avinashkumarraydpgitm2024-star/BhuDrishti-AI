from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.risk_zone import RiskZone
from backend.app.schemas.risk_assessment import RiskAssessmentCreate


def get_risk_zone_by_public_id(
    db: Session,
    public_id: str,
) -> RiskZone | None:
    statement = select(RiskZone).where(
        RiskZone.public_id == public_id
    )

    return db.scalar(statement)


def create_risk_assessment(
    db: Session,
    assessment_data: RiskAssessmentCreate,
) -> RiskAssessment:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=assessment_data.risk_zone_public_id,
    )

    if risk_zone is None:
        raise ValueError(
            "Risk zone not found."
        )

    assessment = RiskAssessment(
        risk_zone_id=risk_zone.id,
        severity=assessment_data.severity,
        risk_probability_percent=(
            assessment_data.risk_probability_percent
        ),
        confidence_percent=assessment_data.confidence_percent,
        forecast_horizon_minutes=(
            assessment_data.forecast_horizon_minutes
        ),
        model_name=assessment_data.model_name.strip(),
        model_version=assessment_data.model_version.strip(),
        dominant_factor=(
            assessment_data.dominant_factor.strip()
            if assessment_data.dominant_factor
            else None
        ),
        explanation=(
            assessment_data.explanation.strip()
            if assessment_data.explanation
            else None
        ),
        assessed_at=assessment_data.assessed_at,
        valid_until=assessment_data.valid_until,
    )

    db.add(assessment)

    try:
        db.commit()
        db.refresh(assessment)

    except Exception:
        db.rollback()
        raise

    return assessment


def get_latest_risk_assessment(
    db: Session,
    *,
    risk_zone_id: int,
    forecast_horizon_minutes: int | None = None,
) -> RiskAssessment | None:
    statement = select(RiskAssessment).where(
        RiskAssessment.risk_zone_id == risk_zone_id
    )

    if forecast_horizon_minutes is not None:
        statement = statement.where(
            RiskAssessment.forecast_horizon_minutes
            == forecast_horizon_minutes
        )

    statement = (
        statement
        .order_by(
            RiskAssessment.assessed_at.desc()
        )
        .limit(1)
    )

    return db.scalar(statement)


def get_risk_assessment_history(
    db: Session,
    *,
    risk_zone_id: int,
    limit: int = 100,
) -> list[RiskAssessment]:
    statement = (
        select(RiskAssessment)
        .where(
            RiskAssessment.risk_zone_id == risk_zone_id
        )
        .order_by(
            RiskAssessment.assessed_at.desc()
        )
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )