from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.village import VillageCreate, VillageRead
from backend.app.services.village_service import (
    create_village,
    get_risk_zone_by_public_id,
    get_village_by_code,
    get_village_by_public_id,
    list_villages,
)


router = APIRouter(
    prefix="/villages",
    tags=["GIS - Villages"],
)


@router.post(
    "",
    response_model=VillageRead,
    status_code=status.HTTP_201_CREATED,
)
def create_village_endpoint(
    payload: VillageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> VillageRead:
    existing = get_village_by_code(
        db=db,
        village_code=payload.village_code,
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Village code already exists.",
        )

    try:
        village = create_village(
            db=db,
            payload=payload,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return VillageRead.model_validate(village)


@router.get(
    "",
    response_model=list[VillageRead],
)
def list_villages_endpoint(
    risk_zone_public_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[VillageRead]:
    risk_zone_id = None

    if risk_zone_public_id is not None:
        risk_zone = get_risk_zone_by_public_id(
            db=db,
            public_id=risk_zone_public_id,
        )

        if risk_zone is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Risk zone not found.",
            )

        risk_zone_id = risk_zone.id

    villages = list_villages(
        db=db,
        risk_zone_id=risk_zone_id,
    )

    return [
        VillageRead.model_validate(village)
        for village in villages
    ]


@router.get(
    "/{public_id}",
    response_model=VillageRead,
)
def get_village_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
) -> VillageRead:
    village = get_village_by_public_id(
        db=db,
        public_id=public_id,
    )

    if village is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Village not found.",
        )

    return VillageRead.model_validate(village)
