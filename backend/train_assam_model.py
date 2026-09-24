from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "synthetic"
    / "assam_landslide_synthetic_100k.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = (
    MODEL_DIR
    / "assam_landslide_model_v1.pkl"
)


NUMERIC_FEATURES = [
    "elevation_m",
    "slope_deg",
    "rainfall_24h_mm",
    "rainfall_72h_mm",
    "rainfall_7d_mm",
    "soil_moisture_index",
    "ndvi",
    "road_distance_km",
    "river_distance_km",
    "road_cutting",
    "deforestation_index",
]


CATEGORICAL_FEATURES = [
    "soil_type",
    "geology",
    "land_cover",
]


FEATURES = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
)

TARGET = "landslide_occurrence"


def main():
    print("Loading Assam synthetic dataset...")

    df = pd.read_csv(DATA_PATH)

    print(
        f"Rows: {len(df):,}"
    )

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y,
        )
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                "passthrough",
                NUMERIC_FEATURES,
            ),
        ]
    )

    classifier = ExtraTreesClassifier(
        n_estimators=400,
        max_depth=24,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "classifier",
                classifier,
            ),
        ]
    )

    print(
        "Training Assam landslide occurrence model..."
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = pipeline.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    print()
    print(
        "Accuracy:",
        round(
            accuracy * 100,
            2,
        ),
        "%",
    )

    print()
    print(
        "Classification report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            digits=4,
        )
    )

    print(
        "Confusion matrix:"
    )

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    artifact = {
        "model": pipeline,
        "features": FEATURES,
        "numeric_features": (
            NUMERIC_FEATURES
        ),
        "categorical_features": (
            CATEGORICAL_FEATURES
        ),
        "target": TARGET,
        "version": (
            "assam-synthetic-v1-extra-trees"
        ),
        "dataset_type": "synthetic",
        "dataset_rows": len(df),
        "warning": (
            "Prototype model trained on synthetic "
            "Assam data. Predictions are not "
            "calibrated real-world landslide "
            "probabilities."
        ),
    }

    joblib.dump(
        artifact,
        MODEL_PATH,
        compress=3,
    )

    print()
    print(
        "Model saved:"
    )

    print(
        MODEL_PATH
    )


if __name__ == "__main__":
    main()
    