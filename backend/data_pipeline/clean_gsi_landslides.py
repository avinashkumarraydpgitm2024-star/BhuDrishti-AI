import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "india_historical_incidents.csv"
OUTPUT_PATH = BASE_DIR / "data" / "india_historical_incidents_clean.csv"

print(f"Input: {INPUT_PATH}")
print(f"Output: {OUTPUT_PATH}")

df = pd.read_csv(INPUT_PATH)

print(f"Loaded rows: {len(df):,}")

TEXT_COLUMNS = [
    "slide_no",
    "state",
    "district",
    "slide_name",
    "nh_sh_location",
    "material_involved",
    "movement_type",
    "history",
]

for col in TEXT_COLUMNS:
    df[col] = (
        df[col]
        .astype("string")
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

print("Basic text cleanup complete.")

STATE_NAME_MAP = {
    "KERALA": "Kerala",
    "KARNATAKA": "Karnataka",
    "MEGHALAYA": "Meghalaya",
    "Tamil nadu": "Tamil Nadu",
    "-Arunachal Pradesh": "Arunachal Pradesh",
}

df["state_normalized"] = df["state"].replace(STATE_NAME_MAP)

print("State normalization complete.")
print(df["state_normalized"].value_counts().to_string())

df["latitude_clean"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude_clean"] = pd.to_numeric(df["longitude"], errors="coerce")

df["coordinate_valid"] = (
    df["latitude_clean"].between(-90, 90)
    & df["longitude_clean"].between(-180, 180)
)

print("Coordinate cleanup complete.")
print("Valid coordinates:", int(df["coordinate_valid"].sum()))
print("Invalid/missing coordinates:", int((~df["coordinate_valid"]).sum()))

def normalize_movement(value):
    if pd.isna(value):
        return "Unknown"

    text = str(value).lower().strip()

    if text in {"", "-", "_", "----", "nil", "n.a.", "-do-"}:
        return "Unknown"

    categories = []

    if "slide" in text or "slump" in text or "landslip" in text or "rotational" in text or "translational" in text or "planar" in text or "wedge" in text:
        categories.append("Slide")
    if "flow" in text:
        categories.append("Flow")
    if "fall" in text or "shooting stone" in text:
        categories.append("Fall")
    if "topple" in text or "toppling" in text:
        categories.append("Topple")
    if "subsiden" in text or "sinking" in text:
        categories.append("Subsidence")
    if "creep" in text:
        categories.append("Creep")
    if "spread" in text:
        categories.append("Spread")
    if "avalan" in text:
        categories.append("Avalanche")
    if "erosion" in text:
        categories.append("Erosion")
    if "crack" in text:
        categories.append("Crack")

    categories = list(dict.fromkeys(categories))

    if not categories:
        return "Other"

    if len(categories) == 1:
        return categories[0]

    return " + ".join(categories)


df["movement_type_normalized"] = df["movement_type"].apply(normalize_movement)

print("Movement normalization code ready.")

def normalize_material(value):
    if pd.isna(value):
        return "Unknown"

    text = str(value).lower().strip()

    if text in {"", "-", "_", "nil", "n.a.", "-do-"}:
        return "Unknown"

    has_rock = "rock" in text or "boulder" in text
    has_debris = "debris" in text or "colluv" in text or "regolith" in text
    has_soil = "soil" in text or "earth" in text
    has_river = "river" in text or "rbm" in text or "fluv" in text
    has_fill = "fill" in text or "muck" in text

    categories = []

    if has_rock:
        categories.append("Rock")
    if has_debris:
        categories.append("Debris")
    if has_soil:
        categories.append("Soil/Earth")
    if has_river:
        categories.append("River-borne")
    if has_fill:
        categories.append("Fill")

    categories = list(dict.fromkeys(categories))

    if not categories:
        return "Other"

    if len(categories) == 1:
        return categories[0]

    return " + ".join(categories)


df["material_normalized"] = df["material_involved"].apply(normalize_material)

print("Material normalization code ready.")

def extract_history_year(value):
    if pd.isna(value):
        return pd.NA

    text = str(value)
    years = pd.Series([text]).str.extract(r"\b((?:19|20)\d{2})\b", expand=False)

    if years.isna().iloc[0]:
        return pd.NA

    return int(years.iloc[0])


df["history_year"] = df["history"].apply(extract_history_year).astype("Int64")

print("History year extraction ready.")
print("Years extracted:", int(df["history_year"].notna().sum()))

df["history_year_future_flag"] = df["history_year"].notna() & (df["history_year"] > 2026)

print("Future history-year flags:", int(df["history_year_future_flag"].sum()))
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"Saved cleaned dataset: {OUTPUT_PATH}")
print(f"Rows saved: {len(df):,}")
print(f"Columns saved: {len(df.columns)}")

print("\nNormalized movement types:")
print(df["movement_type_normalized"].value_counts().to_string())

print("\nNormalized materials:")
print(df["material_normalized"].value_counts().to_string())

