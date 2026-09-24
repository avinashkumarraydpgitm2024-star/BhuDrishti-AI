from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


EXTREME_RAINFALL_THRESHOLD_MM = 64.5


def validate_synthetic_weather_dataset(
    excel_path: str | Path,
) -> dict[str, Any]:
    """Validate the synthetic/project weather workbook without treating it as real evidence."""

    path = Path(excel_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    workbook = pd.ExcelFile(path)

    required_sheets = {"Weather_Data", "Dataset_Info"}
    missing_sheets = sorted(required_sheets.difference(workbook.sheet_names))

    if missing_sheets:
        raise ValueError(
            f"Required workbook sheets missing: {', '.join(missing_sheets)}"
        )

    data = pd.read_excel(path, sheet_name="Weather_Data")
    info = pd.read_excel(path, sheet_name="Dataset_Info")

    metadata = {
        str(row["Field"]).strip(): str(row["Value"]).strip()
        for _, row in info.iterrows()
        if pd.notna(row.get("Field"))
    }

    report: dict[str, Any] = {
        "file": str(path),
        "classification": "synthetic",
        "rows": int(len(data)),
        "columns": int(len(data.columns)),
        "duplicate_rows": int(data.duplicated().sum()),
        "missing_values": {
            column: int(count)
            for column, count in data.isna().sum().items()
        },
        "metadata": metadata,
        "checks": {},
        "warnings": [],
    }

    checks = report["checks"]
    warnings = report["warnings"]

    dataset_type = metadata.get("Dataset type", "")
    checks["synthetic_metadata_confirmed"] = (
        "synthetic" in dataset_type.casefold()
    )

    if not checks["synthetic_metadata_confirmed"]:
        warnings.append(
            "Dataset metadata does not explicitly identify the workbook "
            "as synthetic."
        )

    checks["expected_observations"] = metadata.get("Observations")
    checks["actual_observations"] = int(len(data))
    checks["observation_count_matches_metadata"] = len(data) == 100000

    if not checks["observation_count_matches_metadata"]:
        warnings.append(
            "Weather_Data row count does not match the declared 100,000 observations."
        )

    timestamps = pd.to_datetime(data["Date/Time"], errors="coerce")
    checks["invalid_timestamps"] = int(timestamps.isna().sum())

    valid_timestamps = timestamps.dropna()
    if not valid_timestamps.empty:
        checks["date_min"] = str(valid_timestamps.min())
        checks["date_max"] = str(valid_timestamps.max())

    numeric_ranges = {
        "Rainfall (mm)": (0, None),
        "Temperature (°C)": (-60, 60),
        "Humidity (%)": (0, 100),
        "Latitude": (-90, 90),
        "Longitude": (-180, 180),
    }

    for column, (minimum, maximum) in numeric_ranges.items():
        values = pd.to_numeric(data[column], errors="coerce")

        checks[f"{column}_non_numeric"] = int(values.isna().sum())
        checks[f"{column}_min"] = (
            float(values.min()) if values.notna().any() else None
        )
        checks[f"{column}_max"] = (
            float(values.max()) if values.notna().any() else None
        )

        invalid = values.isna()

        if minimum is not None:
            invalid |= values < minimum

        if maximum is not None:
            invalid |= values > maximum

        checks[f"{column}_invalid_range"] = int(invalid.sum())

    rainfall = pd.to_numeric(data["Rainfall (mm)"], errors="coerce")

    expected_extreme = rainfall >= EXTREME_RAINFALL_THRESHOLD_MM
    actual_extreme = (
        data["Extreme Rainfall"]
        .astype(str)
        .str.strip()
        .str.casefold()
        .eq("yes")
    )

    mismatch_mask = expected_extreme.ne(actual_extreme)

    checks["extreme_threshold_mm_per_hour"] = (
        EXTREME_RAINFALL_THRESHOLD_MM
    )
    checks["expected_extreme_rows"] = int(expected_extreme.sum())
    checks["flagged_extreme_rows"] = int(actual_extreme.sum())
    checks["extreme_flag_mismatches"] = int(mismatch_mask.sum())

    if mismatch_mask.any():
        mismatch_columns = [
            "Rainfall (mm)",
            "Extreme Rainfall",
            "Date/Time",
            "Station",
            "Location",
            "District",
            "State",
            "Latitude",
            "Longitude",
        ]

        report["extreme_flag_anomalies"] = (
            data.loc[mismatch_mask, mismatch_columns]
            .astype(str)
            .to_dict(orient="records")
        )

        warnings.append(
            "Extreme Rainfall flags are inconsistent with the declared "
            ">= 64.5 mm/hour threshold for one or more records."
        )
    else:
        report["extreme_flag_anomalies"] = []

    warnings.append(
        "This workbook is explicitly classified as synthetic/project data "
        "and must not be treated as real-world observations or official evidence."
    )

    report["status"] = (
        "PASS_WITH_WARNINGS"
        if warnings
        else "PASS"
    )

    return report
