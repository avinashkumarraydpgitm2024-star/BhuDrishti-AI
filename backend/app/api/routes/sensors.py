from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.sensor import (
    SensorCreate,
    SensorRead,
)
from backend.app.services.sensor_service import (
    create_sensor,
    get_sensor_by_code,
    get_sensor_by_public_id,
    list_sensors,
)


router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"],
)


@router.post(
    "",
    response_model=SensorRead,
    status_code=status.HTTP_201_CREATED,
)
def register_sensor(
    sensor_data: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
        )
    ),
) -> SensorRead:
    existing_sensor = get_sensor_by_code(
        db=db,
        sensor_code=sensor_data.sensor_code,
    )

    if existing_sensor is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A sensor with this code already exists.",
        )

    try:
        sensor = create_sensor(
            db=db,
            sensor_data=sensor_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return SensorRead.model_validate(sensor)


@router.get(
    "",
    response_model=list[SensorRead],
)
def get_sensors(
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
) -> list[SensorRead]:
    sensors = list_sensors(
        db=db,
        skip=skip,
        limit=limit,
    )

    return [
        SensorRead.model_validate(sensor)
        for sensor in sensors
    ]


@router.get(
    "/{public_id}",
    response_model=SensorRead,
)
def get_sensor(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> SensorRead:
    sensor = get_sensor_by_public_id(
        db=db,
        public_id=public_id,
    )

    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found.",
        )

    return SensorRead.model_validate(sensor)