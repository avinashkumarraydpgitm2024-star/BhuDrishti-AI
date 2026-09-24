from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_LAYERS = {
    "DEM",
    "LandCover",
    "NDVI",
    "Soil",
    "Geology",
    "Roads",
    "Rivers",
    "Boundaries",
}

REQUIRED_MANIFEST_COLUMNS = {
    "layer",
    "source",
    "reference",
    "local_path",
    "acquisition_date",
    "license",
    "sha256",
}


def validate_geo_pipeline(pipeline_root: str | Path) -> dict[str, Any]:
    """Audit a geospatial pipeline delivery and its source provenance."""

    root = Path(pipeline_root)
    manifest_path = root / "metadata" / "source_manifest.csv"

    if not root.exists():
        raise FileNotFoundError(f"Pipeline directory not found: {root}")

    if not manifest_path.exists():
        raise FileNotFoundError(f"Source manifest not found: {manifest_path}")

    manifest = pd.read_csv(manifest_path)

    report: dict[str, Any] = {
        "pipeline_root": str(root),
        "classification": "pipeline_only",
        "manifest_rows": int(len(manifest)),
        "checks": {},
        "warnings": [],
    }

    checks = report["checks"]
    warnings = report["warnings"]

    missing_columns = sorted(
        REQUIRED_MANIFEST_COLUMNS.difference(manifest.columns)
    )
    checks["missing_manifest_columns"] = missing_columns

    if missing_columns:
        warnings.append(
            "Source manifest is missing required provenance columns."
        )

    available_layers = set(
        manifest.get("layer", pd.Series(dtype=str))
        .dropna()
        .astype(str)
        .str.strip()
    )

    missing_layers = sorted(REQUIRED_LAYERS.difference(available_layers))
    checks["required_layers"] = sorted(REQUIRED_LAYERS)
    checks["missing_layers"] = missing_layers

    if missing_layers:
        warnings.append(
            "One or more required geospatial layers are missing from the manifest."
        )

    provenance_fields = ["acquisition_date", "license", "sha256"]
    provenance_missing: dict[str, int] = {}

    for field in provenance_fields:
        if field in manifest.columns:
            provenance_missing[field] = int(
                manifest[field]
                .fillna("")
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )
        else:
            provenance_missing[field] = int(len(manifest))

    checks["missing_provenance_values"] = provenance_missing

    if any(value > 0 for value in provenance_missing.values()):
        warnings.append(
            "Source provenance is incomplete: acquisition date, license, "
            "or SHA-256 values are missing."
        )

    raw_files: list[str] = []

    raw_root = root / "raw"
    if raw_root.exists():
        for path in raw_root.rglob("*"):
            if path.is_file() and path.name != ".gitkeep":
                raw_files.append(str(path.relative_to(root)))

    checks["actual_raw_source_file_count"] = len(raw_files)
    checks["actual_raw_source_files"] = sorted(raw_files)

    if not raw_files:
        warnings.append(
            "No actual raw geospatial source files are present; only the "
            "pipeline/template has been delivered."
        )

    expected_pipeline_files = [
        "config.yaml",
        "README.md",
        "scripts/local_extract.py",
        "scripts/validate_dataset.py",
        "scripts/gee_export.js",
        "metadata/source_manifest.csv",
    ]

    missing_pipeline_files = [
        relative
        for relative in expected_pipeline_files
        if not (root / relative).exists()
    ]

    checks["missing_pipeline_files"] = missing_pipeline_files

    if missing_pipeline_files:
        warnings.append(
            "One or more expected pipeline files are missing."
        )

    sample_outputs = [
        root / "samples" / "northeast_100k.csv",
        root / "samples" / "northeast_100k.geojson",
        root / "samples" / "northeast_100k.parquet",
    ]

    existing_outputs = [
        str(path.relative_to(root))
        for path in sample_outputs
        if path.exists()
    ]

    checks["generated_sample_outputs"] = existing_outputs
    checks["sample_dataset_generated"] = bool(existing_outputs)

    if not existing_outputs:
        warnings.append(
            "No generated Northeast 100K sample dataset is present."
        )

    report["ready_for_extraction"] = (
        not missing_layers
        and not missing_pipeline_files
        and len(raw_files) > 0
        and not any(value > 0 for value in provenance_missing.values())
    )

    report["ready_for_real_data_use"] = False

    warnings.append(
        "Generated records from this workflow must be described as derived "
        "geospatial samples from source layers, not direct field observations."
    )

    report["status"] = (
        "PASS_WITH_WARNINGS" if warnings else "PASS"
    )

    return report


