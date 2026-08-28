from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.alert_delivery import (
    AlertDeliveryCreate,
    AlertDeliveryRead,
)
from backend.app.services.alert_delivery_service import (
    create_alert_delivery,
    get_alert_by_public_id,
    get_delivery_by_public_id,
    list_alert_deliveries,
)


router = APIRouter(
    prefix="/alert-deliveries",
    tags=["Alert Deliveries"],
)


@router.post(
    "",
    response_model=AlertDeliveryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_delivery_endpoint(
    payload: AlertDeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> AlertDeliveryRead:
    try:
        delivery = create_alert_delivery(
            db=db,
            payload=payload,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return AlertDeliveryRead.model_validate(
        delivery
    )


@router.get(
    "",
    response_model=list[AlertDeliveryRead],
)
def list_deliveries_endpoint(
    alert_public_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> list[AlertDeliveryRead]:
    alert_id = None

    if alert_public_id is not None:
        alert = get_alert_by_public_id(
            db=db,
            public_id=alert_public_id,
        )

        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found.",
            )

        alert_id = alert.id

    deliveries = list_alert_deliveries(
        db=db,
        alert_id=alert_id,
        limit=limit,
    )

    return [
        AlertDeliveryRead.model_validate(item)
        for item in deliveries
    ]


@router.get(
    "/{public_id}",
    response_model=AlertDeliveryRead,
)
def get_delivery_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> AlertDeliveryRead:
    delivery = get_delivery_by_public_id(
        db=db,
        public_id=public_id,
    )

    if delivery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert delivery not found.",
        )

    return AlertDeliveryRead.model_validate(
        delivery
    )
