from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.road_segment import (
    RoadSegmentCreate,
    RoadSegmentRead,
)
from backend.app.services.road_segment_service import (
    create_road_segment,
    get_risk_zone_by_public_id,
    get_road_segment_by_code,
    get_road_segment_by_public_id,
    list_road_segments,
)


router = APIRouter(
    prefix="/road-segments",
    tags=["GIS - Roads"],
)


@router.post(
    "",
    response_model=RoadSegmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_road_segment_endpoint(
    payload: RoadSegmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> RoadSegmentRead:
    existing = get_road_segment_by_code(
        db=db,
        road_code=payload.road_code,
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Road segment code already exists.",
        )

    try:
        road_segment = create_road_segment(
            db=db,
            payload=payload,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return RoadSegmentRead.model_validate(
        road_segment
    )


@router.get(
    "",
    response_model=list[RoadSegmentRead],
)
def list_road_segments_endpoint(
    risk_zone_public_id: str | None = Query(default=None),
    blocked_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> list[RoadSegmentRead]:
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

    road_segments = list_road_segments(
        db=db,
        risk_zone_id=risk_zone_id,
        blocked_only=blocked_only,
    )

    return [
        RoadSegmentRead.model_validate(road)
        for road in road_segments
    ]


@router.get(
    "/{public_id}",
    response_model=RoadSegmentRead,
)
def get_road_segment_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
) -> RoadSegmentRead:
    road_segment = get_road_segment_by_public_id(
        db=db,
        public_id=public_id,
    )

    if road_segment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Road segment not found.",
        )

    return RoadSegmentRead.model_validate(
        road_segment
    )
