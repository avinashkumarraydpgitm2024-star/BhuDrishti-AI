import os
import joblib
import pandas as pd

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "risk_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model_v2.pkl")

FEATURES = [
    "rainfall",
    "temperature",
    "humidity",
    "slope",
    "soil_moisture",
    "vegetation",
    "previous_incidents"
]

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training V2 Extra Trees model...")

model = ExtraTreesClassifier(
    n_estimators=300,
    max_depth=22,
    min_samples_split=4,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print("V2 Accuracy:", round(accuracy * 100, 2), "%")
print()
print(classification_report(y_test, predictions))

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": FEATURES,
        "version": "v2-extra-trees"
    },
    MODEL_PATH,
    compress=3
)

print()
print("V2 model saved:")
print(MODEL_PATH)
