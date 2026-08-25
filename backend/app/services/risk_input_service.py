from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.sensor import Sensor, SensorStatus
from backend.app.models.sensor_reading import SensorReading


def get_active_sensors_for_zone(
    db: Session,
    *,
    risk_zone_id: int,
) -> list[Sensor]:
    statement = (
        select(Sensor)
        .where(
            Sensor.risk_zone_id == risk_zone_id,
            Sensor.status == SensorStatus.ACTIVE,
        )
        .order_by(
            Sensor.sensor_code.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def get_latest_valid_reading_for_sensor(
    db: Session,
    *,
    sensor_id: int,
) -> SensorReading | None:
    statement = (
        select(SensorReading)
        .where(
            SensorReading.sensor_id == sensor_id,
            SensorReading.data_quality_status == "valid",
        )
        .order_by(
            SensorReading.recorded_at.desc()
        )
        .limit(1)
    )

    return db.scalar(statement)


def get_latest_valid_readings_for_zone(
    db: Session,
    *,
    risk_zone_id: int,
) -> list[SensorReading]:
    sensors = get_active_sensors_for_zone(
        db=db,
        risk_zone_id=risk_zone_id,
    )

    readings: list[SensorReading] = []

    for sensor in sensors:
        reading = get_latest_valid_reading_for_sensor(
            db=db,
            sensor_id=sensor.id,
        )

        if reading is not None:
            readings.append(reading)

    return readings


def _average(
    values: list[float],
) -> float | None:
    if not values:
        return None

    return sum(values) / len(values)


def aggregate_zone_sensor_inputs(
    db: Session,
    *,
    risk_zone_id: int,
) -> dict[str, float | None]:
    readings = get_latest_valid_readings_for_zone(
        db=db,
        risk_zone_id=risk_zone_id,
    )

    soil_moisture_values = [
        reading.soil_moisture_percent
        for reading in readings
        if reading.soil_moisture_percent is not None
    ]

    rainfall_rate_values = [
        reading.rainfall_rate_mm_hr
        for reading in readings
        if reading.rainfall_rate_mm_hr is not None
    ]

    vibration_values = [
        reading.vibration_level
        for reading in readings
        if reading.vibration_level is not None
    ]

    tilt_values = [
        reading.tilt_degrees
        for reading in readings
        if reading.tilt_degrees is not None
    ]

    return {
        "soil_moisture_percent": _average(
            soil_moisture_values
        ),
        "rainfall_rate_mm_hr": _average(
            rainfall_rate_values
        ),
        "vibration_level": _average(
            vibration_values
        ),
        "tilt_degrees": _average(
            tilt_values
        ),
    }
