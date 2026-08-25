from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.risk_zone import (
    RiskZoneCreate,
    RiskZoneRead,
)
from backend.app.services.risk_zone_service import (
    create_risk_zone,
    get_risk_zone_by_code,
    get_risk_zone_by_public_id,
    list_risk_zones,
)


router = APIRouter(
    prefix="/risk-zones",
    tags=["Risk Zones"],
)


@router.post(
    "",
    response_model=RiskZoneRead,
    status_code=status.HTTP_201_CREATED,
)
def create_zone(
    zone_data: RiskZoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
        )
    ),
) -> RiskZoneRead:
    existing_zone = get_risk_zone_by_code(
        db=db,
        zone_code=zone_data.zone_code,
    )

    if existing_zone is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A risk zone with this code already exists.",
        )

    zone = create_risk_zone(
        db=db,
        zone_data=zone_data,
    )

    return RiskZoneRead.model_validate(zone)


@router.get(
    "",
    response_model=list[RiskZoneRead],
)
def get_zones(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> list[RiskZoneRead]:
    zones = list_risk_zones(
        db=db,
        skip=skip,
        limit=limit,
    )

    return [
        RiskZoneRead.model_validate(zone)
        for zone in zones
    ]


@router.get(
    "/{public_id}",
    response_model=RiskZoneRead,
)
def get_zone(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> RiskZoneRead:
    zone = get_risk_zone_by_public_id(
        db=db,
        public_id=public_id,
    )

    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    return RiskZoneRead.model_validate(zone)
