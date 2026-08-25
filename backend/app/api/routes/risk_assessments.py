from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.risk_assessment import RiskAssessmentRead
from backend.app.services.risk_assessment_service import (
    get_risk_zone_by_public_id,
)
from backend.app.services.risk_orchestrator_service import (
    run_risk_assessment,
)


router = APIRouter(
    prefix="/risk-assessments",
    tags=["Risk Assessments"],
)


@router.post(
    "/generate/{risk_zone_public_id}",
    response_model=RiskAssessmentRead,
    status_code=status.HTTP_201_CREATED,
)
def generate_risk_assessment(
    risk_zone_public_id: str,
    forecast_horizon_minutes: int = Query(
        default=1440,
        ge=60,
        le=10080,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> RiskAssessmentRead:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=risk_zone_public_id,
    )

    if risk_zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    try:
        assessment = run_risk_assessment(
            db=db,
            risk_zone=risk_zone,
            forecast_horizon_minutes=(
                forecast_horizon_minutes
            ),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return RiskAssessmentRead.model_validate(
        assessment
    )
@router.get(
    "/latest/{risk_zone_public_id}",
    response_model=RiskAssessmentRead,
)
def get_latest_assessment(
    risk_zone_public_id: str,
    forecast_horizon_minutes: int | None = Query(
        default=None,
        ge=0,
        le=10080,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> RiskAssessmentRead:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=risk_zone_public_id,
    )

    if risk_zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    from backend.app.services.risk_assessment_service import (
        get_latest_risk_assessment,
    )

    assessment = get_latest_risk_assessment(
        db=db,
        risk_zone_id=risk_zone.id,
        forecast_horizon_minutes=forecast_horizon_minutes,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found.",
        )

    return RiskAssessmentRead.model_validate(
        assessment
    )


@router.get(
    "/history/{risk_zone_public_id}",
    response_model=list[RiskAssessmentRead],
)
def get_assessment_history(
    risk_zone_public_id: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> list[RiskAssessmentRead]:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=risk_zone_public_id,
    )

    if risk_zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    from backend.app.services.risk_assessment_service import (
        get_risk_assessment_history,
    )

    assessments = get_risk_assessment_history(
        db=db,
        risk_zone_id=risk_zone.id,
        limit=limit,
    )

    return [
        RiskAssessmentRead.model_validate(item)
        for item in assessments
    ]