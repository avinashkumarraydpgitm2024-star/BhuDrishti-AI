from backend.app.services.risk_engine_service import (
    RiskEngineInput,
    calculate_baseline_risk,
)


def test_satellite_data_increases_confidence():
    without_satellite = calculate_baseline_risk(
        RiskEngineInput(
            slope_degrees=38,
        )
    )

    with_satellite = calculate_baseline_risk(
        RiskEngineInput(
            slope_degrees=38,
            satellite_ndvi=0.45,
            satellite_ndwi=-0.30,
            satellite_soil_moisture_index=0.41,
        )
    )

    assert (
        with_satellite.confidence_percent
        > without_satellite.confidence_percent
    )
def test_partial_satellite_data_increases_confidence():
    from backend.app.services.risk_engine_service import (
        RiskEngineInput,
        calculate_baseline_risk,
    )

    without_satellite = calculate_baseline_risk(
        RiskEngineInput(slope_degrees=38)
    )

    with_ndvi = calculate_baseline_risk(
        RiskEngineInput(
            slope_degrees=38,
            satellite_ndvi=0.45,
        )
    )

    assert (
        with_ndvi.confidence_percent
        > without_satellite.confidence_percent
    )
