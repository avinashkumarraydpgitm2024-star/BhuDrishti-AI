import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "risk_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model_v2.pkl")

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

saved = joblib.load(MODEL_PATH)

model = saved["model"]
features = saved["features"]

X = df[features]
y = df["risk"]

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Running evaluation...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print("Accuracy:", round(accuracy * 100, 2), "%")

print()
print("Classification Report:")
print(classification_report(y_test, predictions))

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

