from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.gis import GISMapDataRead
from backend.app.services.gis_service import build_gis_map_data
from backend.app.services.risk_zone_service import (
    get_risk_zone_by_public_id,
)


router = APIRouter(
    prefix="/gis",
    tags=["GIS"],
)


@router.get(
    "/map-data/{risk_zone_public_id}",
    response_model=GISMapDataRead,
)
def get_gis_map_data(
    risk_zone_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> GISMapDataRead:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=risk_zone_public_id,
    )

    if risk_zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found.",
        )

    data = build_gis_map_data(
        db=db,
        risk_zone=risk_zone,
    )

    return GISMapDataRead.model_validate(data)
