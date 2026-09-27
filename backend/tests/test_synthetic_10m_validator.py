from pathlib import Path

from openpyxl import Workbook

import backend.data_pipeline.validators.synthetic_10m_validator as validator


def _create_landslide_workbook(
    path: Path,
    *,
    origin: str = "SYNTHETIC_PIPELINE_TEST",
    latitude: float = 26.1,
) -> None:
    headers = validator.EXPECTED_SCHEMAS[
        "01_Landslide_10L.xlsx"
    ]

    rows = [
        {
            "Record_ID": "LS-001",
            "State": "Assam",
            "District": "Cachar",
            "Location_Ref": "TEST-A",
            "Latitude": latitude,
            "Longitude": 92.8,
            "Observation_Date": "2026-01-01",
            "Landslide_Type": "Debris Slide",
            "Trigger": "Rainfall",
            "Slope_deg": 30.0,
            "Elevation_m": 300.0,
            "Lithology": "Sandstone",
            "Soil_Moisture_pct": 60.0,
            "Rain_24h_mm": 80.0,
            "Rain_72h_mm": 180.0,
            "Road_Distance_m": 100.0,
            "River_Distance_m": 500.0,
            "Susceptibility_Class": "High",
            "Event_Label": 1,
            "Source_Code": "SYN-TEST",
            "Data_Origin": origin,
        },
        {
            "Record_ID": "LS-002",
            "State": "Assam",
            "District": "Cachar",
            "Location_Ref": "TEST-B",
            "Latitude": 26.2,
            "Longitude": 92.9,
            "Observation_Date": "2026-01-02",
            "Landslide_Type": "Rock Fall",
            "Trigger": "Rainfall",
            "Slope_deg": 45.0,
            "Elevation_m": 450.0,
            "Lithology": "Shale",
            "Soil_Moisture_pct": 70.0,
            "Rain_24h_mm": 120.0,
            "Rain_72h_mm": 260.0,
            "Road_Distance_m": 50.0,
            "River_Distance_m": 300.0,
            "Susceptibility_Class": "Very High",
            "Event_Label": 1,
            "Source_Code": "SYN-TEST",
            "Data_Origin": origin,
        },
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    ws.append(headers)

    for record in rows:
        ws.append(
            [
                record.get(column)
                for column in headers
            ]
        )

    wb.save(path)


def test_valid_synthetic_workbook_passes(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        validator,
        "EXPECTED_ROWS",
        2,
    )

    path = tmp_path / "01_Landslide_10L.xlsx"

    _create_landslide_workbook(path)

    report = validator.validate_workbook(
        path,
        sample_rows=2,
    )

    assert report["status"] == "PASS"
    assert report["actual_rows"] == 2
    assert report["sample_rows_checked"] == 2
    assert report["duplicate_ids_in_sample"] == 0
    assert report["invalid_coordinates_in_sample"] == 0
    assert report["real_world_evidence_eligible"] is False


def test_wrong_data_origin_is_rejected(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        validator,
        "EXPECTED_ROWS",
        2,
    )

    path = tmp_path / "01_Landslide_10L.xlsx"

    _create_landslide_workbook(
        path,
        origin="REAL_OFFICIAL_DATA",
    )

    report = validator.validate_workbook(
        path,
        sample_rows=2,
    )

    assert report["status"] == "FAIL"

    assert any(
        "Data_Origin=SYNTHETIC_PIPELINE_TEST"
        in error
        for error in report["errors"]
    )


def test_invalid_coordinate_is_detected(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        validator,
        "EXPECTED_ROWS",
        2,
    )

    path = tmp_path / "01_Landslide_10L.xlsx"

    _create_landslide_workbook(
        path,
        latitude=120.0,
    )

    report = validator.validate_workbook(
        path,
        sample_rows=2,
    )

    assert report["status"] == "FAIL"
    assert report["invalid_coordinates_in_sample"] == 1
