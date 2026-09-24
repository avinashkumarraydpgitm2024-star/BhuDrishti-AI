from backend.data_pipeline.india_spatial_index import get_india_spatial_evidence
from backend.data_pipeline.india_spatial_index import get_india_spatial_evidence
import os
import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.risk_explainer import explain_risk, get_top_risk_factors


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model_v2.pkl")

saved = joblib.load(MODEL_PATH)

model = saved["model"]
features = saved["features"]
model_version = saved.get("version", "unknown")


app = FastAPI(
    title="Bhudrishti AI API",
    version="1.0.0"
)


class RiskInput(BaseModel):
    rainfall: float = Field(ge=0, le=500)
    temperature: float = Field(ge=-50, le=60)
    humidity: float = Field(ge=0, le=100)
    slope: float = Field(ge=0, le=90)
    soil_moisture: float = Field(ge=0, le=100)
    vegetation: float = Field(ge=0, le=100)
    previous_incidents: int = Field(ge=0, le=100)


@app.get("/")
def home():
    return {
        "project": "Bhudrishti AI",
        "status": "online",
        "model_loaded": True
    }


@app.post("/predict-risk")
def predict_risk(data: RiskInput):

    input_data = pd.DataFrame([{
        "rainfall": data.rainfall,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "slope": data.slope,
        "soil_moisture": data.soil_moisture,
        "vegetation": data.vegetation,
        "previous_incidents": data.previous_incidents
    }])

    input_data = input_data[features]

    prediction = int(model.predict(input_data)[0])
    probabilities = model.predict_proba(input_data)[0]

    labels = {
        0: "LOW",
        1: "MODERATE",
        2: "HIGH",
        3: "CRITICAL"
    }

    probability_output = {}

    for risk_class, probability in zip(model.classes_, probabilities):
        probability_output[labels[int(risk_class)]] = round(
            float(probability) * 100,
            2
        )

    risk_score = 0.0

    for risk_class, probability in zip(model.classes_, probabilities):
        risk_score += (int(risk_class) / 3) * float(probability)

    risk_score = round(risk_score * 100, 2)

    risk_factors = explain_risk(data)
    top_risk_factors = get_top_risk_factors(risk_factors)

    return {
        "risk_class": prediction,
        "risk_level": labels[prediction],
        "risk_score": risk_score,
        "risk_factors": risk_factors,
        "top_risk_factors": top_risk_factors,
        "probabilities": probability_output
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_version": model_version,
        "service": "Bhudrishti AI Risk Engine"
    }












