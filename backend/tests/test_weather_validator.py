import pandas as pd

from backend.data_pipeline.validators.weather_validator import (
    validate_weather_dataset,
)


def test_weather_validator_valid_dataset(tmp_path):
    dataset = pd.DataFrame(
        {
            "Date/Time": [
                "01-01-2023 00:00",
                "01-01-2023 01:00",
            ],
            "date": ["01-01-2023", "01-01-2023"],
            "location": ["Test Station", "Test Station"],
            "latitude": [23.8, 23.8],
            "longitude": [91.3, 91.3],
            "temperature_C": [20.0, 21.0],
            "relative_humidity_percent": [80.0, 78.0],
            "rainfall_mm": [5.0, 7.0],
            "daily_rainfall_mm": [12.0, 12.0],
            "extreme_rainfall_flag": [0, 0],
            "source": ["test_fixture", "test_fixture"],
        }
    )

    path = tmp_path / "weather.csv"
    dataset.to_csv(path, index=False)

    report = validate_weather_dataset(path)

    assert report["rows"] == 2
    assert report["duplicate_rows"] == 0
    assert report["checks"]["invalid_timestamps"] == 0
    assert report["checks"]["invalid_latitude"] == 0
    assert report["checks"]["invalid_longitude"] == 0
    assert report["checks"]["daily_rainfall_groups"] == 1
    assert report["checks"]["daily_rainfall_mismatches"] == 0


def test_weather_validator_detects_daily_rainfall_mismatch(tmp_path):
    dataset = pd.DataFrame(
        {
            "Date/Time": [
                "01-01-2023 00:00",
                "01-01-2023 01:00",
            ],
            "date": ["01-01-2023", "01-01-2023"],
            "location": ["Test Station", "Test Station"],
            "latitude": [23.8, 23.8],
            "longitude": [91.3, 91.3],
            "temperature_C": [20.0, 21.0],
            "relative_humidity_percent": [80.0, 78.0],
            "rainfall_mm": [5.0, 7.0],
            "daily_rainfall_mm": [20.0, 20.0],
            "extreme_rainfall_flag": [0, 0],
            "source": ["test_fixture", "test_fixture"],
        }
    )

    path = tmp_path / "weather_bad.csv"
    dataset.to_csv(path, index=False)

    report = validate_weather_dataset(path)

    assert report["checks"]["daily_rainfall_mismatches"] == 1
    assert any(
        "Hourly rainfall totals do not match" in warning
        for warning in report["warnings"]
    )
