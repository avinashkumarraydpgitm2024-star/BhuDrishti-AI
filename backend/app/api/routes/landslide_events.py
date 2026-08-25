from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.landslide_event import (
    LandslideEventCreate,
    LandslideEventRead,
)
from backend.app.services.landslide_event_service import (
    create_landslide_event,
)


router = APIRouter(
    prefix="/landslide-events",
    tags=["Landslide Events"],
)


@router.post(
    "",
    response_model=LandslideEventRead,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event_data: LandslideEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> LandslideEventRead:
    try:
        event = create_landslide_event(
            db=db,
            event_data=event_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return LandslideEventRead.model_validate(
        event
    )
from fastapi import Query

from backend.app.services.landslide_event_service import (
    get_landslide_event_by_public_id,
    list_landslide_events,
)


@router.get(
    "",
    response_model=list[LandslideEventRead],
)
def get_landslide_events(
    state: str | None = Query(
        default=None,
        max_length=100,
    ),
    district: str | None = Query(
        default=None,
        max_length=100,
    ),
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
) -> list[LandslideEventRead]:
    events = list_landslide_events(
        db=db,
        state=state,
        district=district,
        limit=limit,
    )

    return [
        LandslideEventRead.model_validate(event)
        for event in events
    ]


@router.get(
    "/{public_id}",
    response_model=LandslideEventRead,
)
def get_landslide_event(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> LandslideEventRead:
    event = get_landslide_event_by_public_id(
        db=db,
        public_id=public_id,
    )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Landslide event not found.",
        )

    return LandslideEventRead.model_validate(
        event
    )