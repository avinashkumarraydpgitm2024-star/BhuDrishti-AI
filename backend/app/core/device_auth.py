from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.device_security import verify_device_api_key
from backend.app.models.sensor import Sensor
from backend.app.services.sensor_service import get_sensor_by_public_id


def authenticate_sensor_device(
    x_sensor_id: str = Header(
        ...,
        alias="X-Sensor-ID",
    ),
    x_device_api_key: str = Header(
        ...,
        alias="X-Device-API-Key",
    ),
    db: Session = Depends(get_db),
) -> Sensor:
    sensor = get_sensor_by_public_id(
        db=db,
        public_id=x_sensor_id,
    )

    if (
        sensor is None
        or sensor.device_api_key_hash is None
        or not verify_device_api_key(
            x_device_api_key,
            sensor.device_api_key_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device credentials.",
        )

    return sensor
