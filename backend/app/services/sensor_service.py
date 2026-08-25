from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.models.sensor import Sensor
from backend.app.schemas.sensor import SensorCreate


def get_sensor_by_code(
    db: Session,
    sensor_code: str,
) -> Sensor | None:
    normalized_code = sensor_code.strip().upper()

    statement = select(Sensor).where(
        Sensor.sensor_code == normalized_code
    )

    return db.scalar(statement)


def get_sensor_by_public_id(
    db: Session,
    public_id: str,
) -> Sensor | None:
    statement = select(Sensor).where(
        Sensor.public_id == public_id
    )

    return db.scalar(statement)


def get_risk_zone_by_public_id(
    db: Session,
    public_id: str,
) -> RiskZone | None:
    statement = select(RiskZone).where(
        RiskZone.public_id == public_id
    )

    return db.scalar(statement)


def create_sensor(
    db: Session,
    sensor_data: SensorCreate,
) -> Sensor:
    risk_zone_id: int | None = None

    if sensor_data.risk_zone_public_id:
        risk_zone = get_risk_zone_by_public_id(
            db=db,
            public_id=sensor_data.risk_zone_public_id,
        )

        if risk_zone is None:
            raise ValueError(
                "Risk zone not found."
            )

        risk_zone_id = risk_zone.id

    sensor = Sensor(
        sensor_code=sensor_data.sensor_code.strip().upper(),
        name=sensor_data.name.strip(),
        sensor_type=sensor_data.sensor_type,
        risk_zone_id=risk_zone_id,
        latitude=sensor_data.latitude,
        longitude=sensor_data.longitude,
        elevation_m=sensor_data.elevation_m,
        installation_depth_cm=sensor_data.installation_depth_cm,
        firmware_version=(
            sensor_data.firmware_version.strip()
            if sensor_data.firmware_version
            else None
        ),
        installed_at=datetime.now(timezone.utc),
    )

    db.add(sensor)

    try:
        db.commit()
        db.refresh(sensor)
    except Exception:
        db.rollback()
        raise

    return sensor


def list_sensors(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[Sensor]:
    statement = (
        select(Sensor)
        .order_by(
            Sensor.sensor_code
        )
        .offset(skip)
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )