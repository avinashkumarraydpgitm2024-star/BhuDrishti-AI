from dataclasses import dataclass

from backend.app.models.risk_assessment import RiskSeverity


@dataclass
class RiskEngineInput:
    rainfall_rate_mm_hr: float | None = None
    rainfall_24h_mm: float | None = None
    soil_moisture_percent: float | None = None
    slope_degrees: float | None = None
    vibration_level: float | None = None
    tilt_degrees: float | None = None
    precipitation_probability_percent: float | None = None
    historical_risk_score: float | None = None
    satellite_ndwi: float | None = None
    satellite_soil_moisture_index: float | None = None
    satellite_ndvi: float | None = None


@dataclass
class RiskEngineResult:
    risk_probability_percent: float
    severity: RiskSeverity
    confidence_percent: float
    dominant_factor: str
    explanation: str


def _normalize(
    value: float | None,
    *,
    minimum: float,
    maximum: float,
) -> float:
    if value is None:
        return 0.0

    if maximum <= minimum:
        return 0.0

    normalized = (
        (value - minimum)
        / (maximum - minimum)
    )

    return max(
        0.0,
        min(
            1.0,
            normalized,
        ),
    )


def _severity_from_probability(
    probability: float,
) -> RiskSeverity:
    if probability >= 90:
        return RiskSeverity.CRITICAL

    if probability >= 75:
        return RiskSeverity.VERY_HIGH

    if probability >= 55:
        return RiskSeverity.HIGH

    if probability >= 30:
        return RiskSeverity.MODERATE

    return RiskSeverity.LOW


def calculate_baseline_risk(
    data: RiskEngineInput,
) -> RiskEngineResult:
    rainfall_rate_score = _normalize(
        data.rainfall_rate_mm_hr,
        minimum=0,
        maximum=80,
    )

    rainfall_24h_score = _normalize(
        data.rainfall_24h_mm,
        minimum=0,
        maximum=250,
    )

    soil_moisture_score = _normalize(
        data.soil_moisture_percent,
        minimum=20,
        maximum=100,
    )

    slope_score = _normalize(
        data.slope_degrees,
        minimum=5,
        maximum=55,
    )

    vibration_score = _normalize(
        data.vibration_level,
        minimum=0,
        maximum=10,
    )

    tilt_score = _normalize(
        abs(data.tilt_degrees)
        if data.tilt_degrees is not None
        else None,
        minimum=0,
        maximum=10,
    )

    precipitation_probability_score = _normalize(
        data.precipitation_probability_percent,
        minimum=0,
        maximum=100,
    )

    historical_risk_score = _normalize(
        data.historical_risk_score,
        minimum=0,
        maximum=1,
    )
    satellite_ndwi_score = _normalize(
        data.satellite_ndwi,
        minimum=-1,
        maximum=1,
    )

    satellite_soil_moisture_score = _normalize(
        data.satellite_soil_moisture_index,
        minimum=0,
        maximum=1,
    )

    satellite_ndvi_score = _normalize(
        data.satellite_ndvi,
        minimum=-1,
        maximum=1,
    )


    satellite_vegetation_stress_score = (
        1 - satellite_ndvi_score
        if satellite_ndvi_score is not None
        else None
    )

    weighted_scores = {
        "rainfall_rate": rainfall_rate_score * 0.15,
        "rainfall_24h": rainfall_24h_score * 0.15,
        "soil_moisture": soil_moisture_score * 0.15,
        "slope": slope_score * 0.15,
        "historical_risk": historical_risk_score * 0.12,
        "satellite_ndwi": (
            satellite_ndwi_score * 0.05
            if satellite_ndwi_score is not None
            else 0
        ),
        "satellite_soil_moisture": (
            satellite_soil_moisture_score * 0.05
            if satellite_soil_moisture_score is not None
            else 0
        ),
        "satellite_vegetation_stress": (
            satellite_vegetation_stress_score * 0.05
            if satellite_vegetation_stress_score is not None
            else 0
        ),
        "vibration": vibration_score * 0.05,
        "tilt": tilt_score * 0.05,
        "precipitation_probability": (
            precipitation_probability_score * 0.03
        ),
    }

    raw_score = sum(
        weighted_scores.values()
    )

    probability = round(
        max(
            0.0,
            min(
                100.0,
                raw_score * 100,
            ),
        ),
        2,
    )

    severity = _severity_from_probability(
        probability
    )

    dominant_factor = max(
        weighted_scores,
        key=weighted_scores.get,
    )

    available_inputs = [
        data.rainfall_rate_mm_hr,
        data.rainfall_24h_mm,
        data.soil_moisture_percent,
        data.slope_degrees,
        data.vibration_level,
        data.tilt_degrees,
        data.precipitation_probability_percent,
        data.historical_risk_score,
    ]
    

    available_count = sum(
        value is not None
        for value in available_inputs
    )

    confidence = round(
        min(
            95.0,
            40.0
            + (
                available_count
                / len(available_inputs)
            )
            * 55.0,
        ),
        2,
    )

    explanation = (
        f"Baseline landslide risk is {probability}% "
        f"with {severity.value} severity. "
        f"The dominant contributing factor is "
        f"{dominant_factor.replace('_', ' ')}."
    )

    return RiskEngineResult(
        risk_probability_percent=probability,
        severity=severity,
        confidence_percent=confidence,
        dominant_factor=dominant_factor,
        explanation=explanation,
    )






