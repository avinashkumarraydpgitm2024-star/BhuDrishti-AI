from backend.app.schemas.sensor_reading import SensorReadingCreate


def evaluate_reading_quality(
    reading_data: SensorReadingCreate,
) -> str:
    suspicious = False

    if (
        reading_data.soil_moisture_percent is not None
        and reading_data.soil_moisture_percent > 95
    ):
        suspicious = True

    if (
        reading_data.rainfall_rate_mm_hr is not None
        and reading_data.rainfall_rate_mm_hr > 300
    ):
        suspicious = True

    if (
        reading_data.tilt_degrees is not None
        and abs(reading_data.tilt_degrees) > 60
    ):
        suspicious = True

    if (
        reading_data.signal_strength_dbm is not None
        and reading_data.signal_strength_dbm < -120
    ):
        suspicious = True

    return "suspect" if suspicious else "valid"