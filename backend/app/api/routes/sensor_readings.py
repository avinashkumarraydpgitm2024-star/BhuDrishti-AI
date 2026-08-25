from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import require_roles
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.sensor_reading import (
    SensorReadingCreate,
    SensorReadingRead,
)
from backend.app.services.sensor_reading_service import (
    create_sensor_reading,
    get_latest_sensor_reading,
    get_sensor_by_public_id,
    get_sensor_reading_history,
)


router = APIRouter(
    prefix="/sensor-readings",
    tags=["Sensor Readings"],
)


@router.post(
    "",
    response_model=SensorReadingRead,
    status_code=status.HTTP_201_CREATED,
)
def submit_sensor_reading(
    reading_data: SensorReadingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> SensorReadingRead:
    try:
        reading = create_sensor_reading(
            db=db,
            reading_data=reading_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return SensorReadingRead.model_validate(reading)


@router.get(
    "/{sensor_public_id}/latest",
    response_model=SensorReadingRead,
)
def get_latest_reading(
    sensor_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
            "field_officer",
        )
    ),
) -> SensorReadingRead:
    sensor = get_sensor_by_public_id(
        db=db,
        public_id=sensor_public_id,
    )

    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found.",
        )

    reading = get_latest_sensor_reading(
        db=db,
        sensor_id=sensor.id,
    )

    if reading is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reading found for this sensor.",
        )

    return SensorReadingRead.model_validate(reading)


@router.get(
    "/{sensor_public_id}/history",
    response_model=list[SensorReadingRead],
)
def get_reading_history(
    sensor_public_id: str,
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
) -> list[SensorReadingRead]:
    sensor = get_sensor_by_public_id(
        db=db,
        public_id=sensor_public_id,
    )

    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found.",
        )

    readings = get_sensor_reading_history(
        db=db,
        sensor_id=sensor.id,
        limit=limit,
    )

    return [
        SensorReadingRead.model_validate(reading)
        for reading in readings
    ]