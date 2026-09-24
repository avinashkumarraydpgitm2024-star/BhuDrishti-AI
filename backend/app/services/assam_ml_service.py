from pathlib import Path
from typing import Any

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "assam_landslide_model_v1.pkl"
)

_model_artifact: dict[str, Any] | None = None


def load_assam_model() -> dict[str, Any]:
    global _model_artifact

    if _model_artifact is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Assam ML model not found: {MODEL_PATH}"
            )

        _model_artifact = joblib.load(
            MODEL_PATH
        )

    return _model_artifact


def predict_assam_landslide(
    *,
    elevation_m: float,
    slope_deg: float,
    rainfall_24h_mm: float,
    rainfall_72h_mm: float,
    rainfall_7d_mm: float,
    soil_moisture_index: float,
    ndvi: float,
    road_distance_km: float,
    river_distance_km: float,
    road_cutting: int,
    deforestation_index: float,
    soil_type: str,
    geology: str,
    land_cover: str,
) -> dict[str, Any]:

    artifact = load_assam_model()

    features = artifact["features"]

    input_data = {
        "elevation_m": elevation_m,
        "slope_deg": slope_deg,
        "rainfall_24h_mm": rainfall_24h_mm,
        "rainfall_72h_mm": rainfall_72h_mm,
        "rainfall_7d_mm": rainfall_7d_mm,
        "soil_moisture_index": soil_moisture_index,
        "ndvi": ndvi,
        "road_distance_km": road_distance_km,
        "river_distance_km": river_distance_km,
        "road_cutting": road_cutting,
        "deforestation_index": deforestation_index,
        "soil_type": soil_type,
        "geology": geology,
        "land_cover": land_cover,
    }

    frame = pd.DataFrame(
        [input_data],
        columns=features,
    )

    model = artifact["model"]

    prediction = int(
        model.predict(frame)[0]
    )

    probabilities = model.predict_proba(
        frame
    )[0]

    classes = list(
        model.classes_
    )

    positive_probability = 0.0

    if 1 in classes:
        positive_index = classes.index(1)

        positive_probability = float(
            probabilities[positive_index]
        )

    probability_percent = round(
        positive_probability * 100,
        2,
    )

    return {
        "prediction": prediction,
        "landslide_detected": (
            prediction == 1
        ),
        "probability_percent": (
            probability_percent
        ),
        "model_version": artifact.get(
            "version",
            "assam-synthetic-v1",
        ),
        "dataset_type": artifact.get(
            "dataset_type",
            "synthetic",
        ),
    }
