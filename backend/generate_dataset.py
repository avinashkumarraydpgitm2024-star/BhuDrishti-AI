import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

ROWS = 150000

rainfall = np.random.gamma(2.2, 30, ROWS).clip(0, 300)
temperature = np.random.normal(24, 7, ROWS).clip(-5, 48)
humidity = np.random.normal(70, 18, ROWS).clip(15, 100)
slope = np.random.beta(2, 3, ROWS) * 75
soil_moisture = np.random.normal(55, 22, ROWS).clip(0, 100)
vegetation = np.random.normal(55, 25, ROWS).clip(0, 100)
previous_incidents = np.random.poisson(1.5, ROWS).clip(0, 15)

risk_score = (
    rainfall * 0.22 +
    humidity * 0.08 +
    slope * 0.28 +
    soil_moisture * 0.22 +
    (100 - vegetation) * 0.12 +
    previous_incidents * 4.5
)

risk_score += np.random.normal(0, 8, ROWS)

risk = np.select(
    [
        risk_score < 35,
        risk_score < 55,
        risk_score < 75
    ],
    [
        0,
        1,
        2
    ],
    default=3
)

df = pd.DataFrame({
    "rainfall": rainfall.round(2),
    "temperature": temperature.round(2),
    "humidity": humidity.round(2),
    "slope": slope.round(2),
    "soil_moisture": soil_moisture.round(2),
    "vegetation": vegetation.round(2),
    "previous_incidents": previous_incidents,
    "risk": risk
})

output = Path("backend/data/risk_data.csv")
output.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output, index=False)

print("Bhudrishti dataset created successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print()
print(df["risk"].value_counts().sort_index())
print()
print("Saved at:", output)
