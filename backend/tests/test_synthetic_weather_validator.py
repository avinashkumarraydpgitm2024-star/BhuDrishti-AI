from pathlib import Path

import pandas as pd

from backend.data_pipeline.validators.synthetic_weather_validator import (
    validate_synthetic_weather_dataset,
)


def _create_workbook(path: Path, rainfall: float, extreme_flag: str) -> None:
    weather = pd.DataFrame(
        {
            "Rainfall (mm)": [rainfall],
            "Temperature (°C)": [24.0],
            "Humidity (%)": [80.0],
            "Extreme Rainfall": [extreme_flag],
            "Date/Time": ["2025-07-08 07:00:00"],
            "Station": ["Test Station"],
            "Location": ["Test Location"],
            "District": ["Test District"],
            "State": ["Assam"],
            "Latitude": [26.0],
            "Longitude": [92.0],
        }
    )

    info = pd.DataFrame(
        {
            "Field": [
                "Dataset type",
                "Observations",
                "Region",
                "Time coverage",
                "Rainfall unit",
                "Extreme rainfall threshold",
            ],
            "Value": [
                "Synthetic/project dataset",
                "100,000",
                "Northeast India",
                "2021-2025 (hourly timestamps sampled)",
                "mm",
                ">= 64.5 mm/hour",
            ],
        }
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        weather.to_excel(writer, sheet_name="Weather_Data", index=False)
        info.to_excel(writer, sheet_name="Dataset_Info", index=False)


def test_extreme_threshold_match(tmp_path: Path) -> None:
    path = tmp_path / "valid.xlsx"
    _create_workbook(path, rainfall=64.5, extreme_flag="Yes")

    report = validate_synthetic_weather_dataset(path)

    assert report["classification"] == "synthetic"
    assert report["checks"]["synthetic_metadata_confirmed"] is True
    assert report["checks"]["expected_extreme_rows"] == 1
    assert report["checks"]["flagged_extreme_rows"] == 1
    assert report["checks"]["extreme_flag_mismatches"] == 0


def test_extreme_threshold_mismatch_is_detected(tmp_path: Path) -> None:
    path = tmp_path / "mismatch.xlsx"
    _create_workbook(path, rainfall=64.5, extreme_flag="No")

    report = validate_synthetic_weather_dataset(path)

    assert report["checks"]["expected_extreme_rows"] == 1
    assert report["checks"]["flagged_extreme_rows"] == 0
    assert report["checks"]["extreme_flag_mismatches"] == 1
    assert len(report["extreme_flag_anomalies"]) == 1
    assert any(
        "Extreme Rainfall flags are inconsistent" in warning
        for warning in report["warnings"]
    )
