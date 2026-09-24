from pathlib import Path

import pandas as pd

from backend.data_pipeline.validators.geo_pipeline_validator import (
    validate_geo_pipeline,
)


def _create_pipeline(root: Path, include_raw_file: bool = False) -> None:
    required_files = [
        "config.yaml",
        "README.md",
        "scripts/local_extract.py",
        "scripts/validate_dataset.py",
        "scripts/gee_export.js",
    ]

    for relative in required_files:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test", encoding="utf-8")

    layers = [
        ("DEM", "raw/dem/"),
        ("LandCover", "raw/landcover/"),
        ("NDVI", "raw/ndvi/"),
        ("Soil", "raw/soil/"),
        ("Geology", "raw/geology/"),
        ("Roads", "raw/roads/"),
        ("Rivers", "raw/rivers/"),
        ("Boundaries", "raw/boundaries/"),
    ]

    manifest = pd.DataFrame(
        {
            "layer": [x[0] for x in layers],
            "source": ["Test Source"] * 8,
            "reference": ["https://example.com"] * 8,
            "local_path": [x[1] for x in layers],
            "acquisition_date": [None] * 8,
            "license": [None] * 8,
            "sha256": [None] * 8,
        }
    )

    manifest_path = root / "metadata" / "source_manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(manifest_path, index=False)

    if include_raw_file:
        raw_file = root / "raw" / "dem" / "dem.tif"
        raw_file.parent.mkdir(parents=True, exist_ok=True)
        raw_file.write_bytes(b"test")


def test_pipeline_only_delivery_is_detected(tmp_path: Path) -> None:
    root = tmp_path / "pipeline"
    _create_pipeline(root)

    report = validate_geo_pipeline(root)

    assert report["classification"] == "pipeline_only"
    assert report["checks"]["missing_layers"] == []
    assert report["checks"]["actual_raw_source_file_count"] == 0
    assert report["checks"]["missing_provenance_values"] == {
        "acquisition_date": 8,
        "license": 8,
        "sha256": 8,
    }
    assert report["ready_for_extraction"] is False
    assert report["ready_for_real_data_use"] is False
    assert report["status"] == "PASS_WITH_WARNINGS"


def test_raw_file_alone_does_not_make_pipeline_ready(tmp_path: Path) -> None:
    root = tmp_path / "pipeline"
    _create_pipeline(root, include_raw_file=True)

    report = validate_geo_pipeline(root)

    assert report["checks"]["actual_raw_source_file_count"] == 1
    assert report["ready_for_extraction"] is False
    assert report["ready_for_real_data_use"] is False
