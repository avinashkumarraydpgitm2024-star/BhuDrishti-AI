from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.alert import AlertRead
from backend.app.services.alert_service import (
    get_alert_by_public_id,
    get_risk_zone_by_public_id,
    list_alerts,
)


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get(
    "",
    response_model=list[AlertRead],
)
def get_alerts(
    risk_zone_public_id: str | None = Query(default=None),
    active_only: bool = Query(default=False),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> list[AlertRead]:
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

    alerts = list_alerts(
        db=db,
        risk_zone_id=risk_zone_id,
        active_only=active_only,
        limit=limit,
    )

    return [
        AlertRead.model_validate(alert)
        for alert in alerts
    ]


@router.get(
    "/{public_id}",
    response_model=AlertRead,
)
def get_alert(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> AlertRead:
    alert = get_alert_by_public_id(
        db=db,
        public_id=public_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return AlertRead.model_validate(alert)

@router.post(
    "/{public_id}/acknowledge",
    response_model=AlertRead,
)
def acknowledge_alert_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> AlertRead:
    from backend.app.services.alert_service import (
        acknowledge_alert,
    )

    alert = get_alert_by_public_id(
        db=db,
        public_id=public_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    try:
        alert = acknowledge_alert(
            db=db,
            alert=alert,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return AlertRead.model_validate(alert)


@router.post(
    "/{public_id}/resolve",
    response_model=AlertRead,
)
def resolve_alert_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
        )
    ),
) -> AlertRead:
    from backend.app.services.alert_service import (
        resolve_alert,
    )

    alert = get_alert_by_public_id(
        db=db,
        public_id=public_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    alert = resolve_alert(
        db=db,
        alert=alert,
    )

    return AlertRead.model_validate(alert)
