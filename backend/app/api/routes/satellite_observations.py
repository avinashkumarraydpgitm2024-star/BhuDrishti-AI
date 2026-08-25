from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.satellite_observation import (
    SatelliteObservationCreate,
    SatelliteObservationRead,
)
from backend.app.services.satellite_observation_service import (
    create_satellite_observation,
    get_latest_satellite_observation_for_zone,
    get_risk_zone_by_public_id,
    get_satellite_observation_history,
)


router = APIRouter(
    prefix="/satellite-observations",
    tags=["Satellite Observations"],
)


@router.post(
    "",
    response_model=SatelliteObservationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_observation(
    observation_data: SatelliteObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> SatelliteObservationRead:
    try:
        observation = create_satellite_observation(
            db=db,
            observation_data=observation_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return SatelliteObservationRead.model_validate(
        observation
    )


@router.get(
    "/latest/{risk_zone_public_id}",
    response_model=SatelliteObservationRead,
)
def get_latest_observation(
    risk_zone_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> SatelliteObservationRead:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=risk_zone_public_id,
    )

    if risk_zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    observation = get_latest_satellite_observation_for_zone(
        db=db,
        risk_zone_id=risk_zone.id,
    )

    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Satellite observation not found.",
        )

    return SatelliteObservationRead.model_validate(
        observation
    )


@router.get(
    "/history/{risk_zone_public_id}",
    response_model=list[SatelliteObservationRead],
)
def get_observation_history(
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
) -> list[SatelliteObservationRead]:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=risk_zone_public_id,
    )

    if risk_zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    observations = get_satellite_observation_history(
        db=db,
        risk_zone_id=risk_zone.id,
        limit=limit,
    )

    return [
        SatelliteObservationRead.model_validate(item)
        for item in observations
    ]