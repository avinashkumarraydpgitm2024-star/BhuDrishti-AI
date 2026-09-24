import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model_v2.pkl")

saved = joblib.load(MODEL_PATH)

model = saved["model"]
features = saved["features"]

test_data = pd.DataFrame([{
    "rainfall": 125,
    "temperature": 19,
    "humidity": 92,
    "slope": 58,
    "soil_moisture": 90,
    "vegetation": 22,
    "previous_incidents": 5
}])

test_data = test_data[features]

prediction = int(model.predict(test_data)[0])
probabilities = model.predict_proba(test_data)[0]

risk_labels = {
    0: "LOW",
    1: "MODERATE",
    2: "HIGH",
    3: "CRITICAL"
}

print()
print("===== BHUDRISHTI AI RISK PREDICTION =====")
print()
print("Risk Class:", prediction)
print("Risk Level:", risk_labels[prediction])
print()
print("Class Probabilities:")

for risk_class, probability in zip(model.classes_, probabilities):
    print(
        risk_labels[int(risk_class)],
        ":",
        round(float(probability) * 100, 2),
        "%"
    )

