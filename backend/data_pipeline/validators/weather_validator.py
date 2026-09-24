from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def validate_weather_dataset(csv_path: str | Path) -> dict[str, Any]:
    """Run structural and quality checks on a weather/rainfall CSV dataset."""

    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    report: dict[str, Any] = {
        "file": str(path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": {
            column: int(count)
            for column, count in df.isna().sum().items()
        },
        "checks": {},
        "warnings": [],
    }

    checks = report["checks"]
    warnings = report["warnings"]

    # Timestamp validation
    timestamp_column = next(
        (c for c in ("Date/Time", "datetime", "timestamp", "date") if c in df.columns),
        None,
    )

    if timestamp_column:
        timestamps = pd.to_datetime(df[timestamp_column], format="%d-%m-%Y %H:%M", errors="coerce")

        checks["timestamp_column"] = timestamp_column
        checks["invalid_timestamps"] = int(timestamps.isna().sum())

        valid_timestamps = timestamps.dropna()
        if not valid_timestamps.empty:
            checks["date_min"] = str(valid_timestamps.min())
            checks["date_max"] = str(valid_timestamps.max())
    else:
        warnings.append("No recognized timestamp column found.")

    # Geographic validation
    if {"latitude", "longitude"}.issubset(df.columns):
        lat = pd.to_numeric(df["latitude"], errors="coerce")
        lon = pd.to_numeric(df["longitude"], errors="coerce")

        checks["invalid_latitude"] = int(
            (lat.isna() | ~lat.between(-90, 90)).sum()
        )
        checks["invalid_longitude"] = int(
            (lon.isna() | ~lon.between(-180, 180)).sum()
        )
    else:
        warnings.append("Latitude/longitude columns are missing.")

    numeric_checks = {
        "temperature_C": (-60, 60),
        "relative_humidity_percent": (0, 100),
        "rainfall_mm": (0, None),
        "daily_rainfall_mm": (0, None),
    }

    for column, (minimum, maximum) in numeric_checks.items():
        if column not in df.columns:
            warnings.append(f"Expected column missing: {column}")
            continue

        values = pd.to_numeric(df[column], errors="coerce")

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

    # Daily rainfall aggregation consistency
    required_daily_columns = {
        "date",
        "location",
        "rainfall_mm",
        "daily_rainfall_mm",
    }

    if required_daily_columns.issubset(df.columns):
        hourly_rain = pd.to_numeric(df["rainfall_mm"], errors="coerce")
        reported_daily = pd.to_numeric(
            df["daily_rainfall_mm"], errors="coerce"
        )

        daily_check = pd.DataFrame({
            "date": df["date"],
            "location": df["location"],
            "hourly_rain": hourly_rain,
            "reported_daily": reported_daily,
        })

        grouped = daily_check.groupby(
            ["date", "location"], dropna=False
        ).agg(
            calculated_daily=("hourly_rain", "sum"),
            reported_daily=("reported_daily", "first"),
        )

        difference = (
            grouped["calculated_daily"] - grouped["reported_daily"]
        ).abs()

        checks["daily_rainfall_groups"] = int(len(grouped))
        checks["daily_rainfall_mismatches"] = int((difference > 0.01).sum())
        checks["daily_rainfall_max_difference_mm"] = float(difference.max())

        if checks["daily_rainfall_mismatches"] > 0:
            warnings.append(
                "Hourly rainfall totals do not match reported daily rainfall "
                "for one or more location-date groups."
            )
    else:
        warnings.append(
            "Daily rainfall aggregation could not be checked because required "
            "date/location/rainfall columns are missing."
        )
    # Extreme rainfall flag sanity check
    if "extreme_rainfall_flag" in df.columns:
        flags = pd.to_numeric(df["extreme_rainfall_flag"], errors="coerce")

        checks["extreme_flag_counts"] = {
            str(key): int(value)
            for key, value in flags.value_counts(dropna=False).items()
        }

        if flags.fillna(0).sum() == 0:
            warnings.append(
                "No rows are marked as extreme rainfall; verify the threshold "
                "and flag-generation methodology."
            )

    # Provenance checks
    provenance_columns = {
        "source",
        "provider",
        "source_url",
        "station_id",
        "dataset",
        "api",
    }

    found_provenance = sorted(provenance_columns.intersection(df.columns))
    checks["provenance_columns_found"] = found_provenance

    if not found_provenance:
        warnings.append(
            "No source/provider provenance columns found. "
            "Dataset provenance must be verified separately."
        )

    report["status"] = (
        "PASS_WITH_WARNINGS"
        if warnings
        else "PASS"
    )

    return report


