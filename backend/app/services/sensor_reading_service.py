from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.sensor import Sensor
from backend.app.models.sensor_reading import SensorReading
from backend.app.schemas.sensor_reading import SensorReadingCreate
from backend.app.services.data_quality_service import evaluate_reading_quality


def get_sensor_by_public_id(
    db: Session,
    public_id: str,
) -> Sensor | None:
    statement = select(Sensor).where(
        Sensor.public_id == public_id
    )

    return db.scalar(statement)


def create_sensor_reading(
    db: Session,
    reading_data: SensorReadingCreate,
) -> SensorReading:
    sensor = get_sensor_by_public_id(
        db=db,
        public_id=reading_data.sensor_public_id,
    )

    if sensor is None:
        raise ValueError(
            "Sensor not found."
        )

    quality_status = evaluate_reading_quality(
        reading_data
    )

    reading = SensorReading(
        sensor_id=sensor.id,
        soil_moisture_percent=reading_data.soil_moisture_percent,
        rainfall_mm=reading_data.rainfall_mm,
        rainfall_rate_mm_hr=reading_data.rainfall_rate_mm_hr,
        tilt_degrees=reading_data.tilt_degrees,
        vibration_level=reading_data.vibration_level,
        temperature_c=reading_data.temperature_c,
        humidity_percent=reading_data.humidity_percent,
        battery_level_percent=reading_data.battery_level_percent,
        signal_strength_dbm=reading_data.signal_strength_dbm,
        data_quality_status=quality_status,
        recorded_at=reading_data.recorded_at,
    )

    # Update sensor's latest operational information.
    sensor.last_seen_at = datetime.now(timezone.utc)

    if reading_data.battery_level_percent is not None:
        sensor.battery_level_percent = (
            reading_data.battery_level_percent
        )

    if reading_data.signal_strength_dbm is not None:
        sensor.signal_strength_dbm = (
            reading_data.signal_strength_dbm
        )

    db.add(reading)

    try:
        db.commit()
        db.refresh(reading)

    except Exception:
        db.rollback()
        raise

    return reading


def get_latest_sensor_reading(
    db: Session,
    sensor_id: int,
) -> SensorReading | None:
    statement = (
        select(SensorReading)
        .where(
            SensorReading.sensor_id == sensor_id
        )
        .order_by(
            SensorReading.recorded_at.desc()
        )
        .limit(1)
    )

    return db.scalar(statement)


def get_sensor_reading_history(
    db: Session,
    sensor_id: int,
    *,
    limit: int = 100,
) -> list[SensorReading]:
    statement = (
        select(SensorReading)
        .where(
            SensorReading.sensor_id == sensor_id
        )
        .order_by(
            SensorReading.recorded_at.desc()
        )
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )



