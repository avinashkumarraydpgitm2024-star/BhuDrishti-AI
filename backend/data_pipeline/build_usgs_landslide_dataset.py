import pandas as pd

from backend.data_pipeline.usgs_landslide_normalizer import (
    categorize_landslide_type
)


SOURCE_PATH = (
    "backend/data/US_Landslide_v3_csv/"
    "US_Landslide_v3_csv/us_ls_v3_point.csv"
)

OUTPUT_PATH = (
    "backend/data/usgs_landslides_clean.csv"
)

REQUIRED_COLUMNS = [
    "USGS_ID",
    "Date_Min",
    "Date_Max",
    "Fatalities",
    "Confidence",
    "LS_Type",
    "Inventory",
    "Inv_URL",
    "Info_Source",
    "Notes",
    "Lat_N",
    "Lon_W"
]


def load_source_data():
    return pd.read_csv(
        SOURCE_PATH,
        usecols=REQUIRED_COLUMNS,
        low_memory=False
    )


def clean_dataset(df):
    cleaned = df.copy()

    cleaned["latitude"] = pd.to_numeric(
        cleaned["Lat_N"],
        errors="coerce"
    )

    cleaned["longitude"] = pd.to_numeric(
        cleaned["Lon_W"],
        errors="coerce"
    )

    cleaned["date_min"] = pd.to_datetime(
        cleaned["Date_Min"],
        errors="coerce",
        format="mixed"
    )

    cleaned["date_max"] = pd.to_datetime(
        cleaned["Date_Max"],
        errors="coerce",
        format="mixed"
    )

    cleaned["landslide_category"] = (
        cleaned["LS_Type"].apply(
            categorize_landslide_type
        )
    )

    return cleaned


def select_output_columns(cleaned):
    output = cleaned[
        [
            "USGS_ID",
            "latitude",
            "longitude",
            "date_min",
            "date_max",
            "Fatalities",
            "Confidence",
            "LS_Type",
            "landslide_category",
            "Inventory",
            "Inv_URL",
            "Info_Source",
            "Notes"
        ]
    ].copy()

    return output


def save_clean_dataset():
    raw = load_source_data()
    cleaned = clean_dataset(raw)
    output = select_output_columns(cleaned)

    output.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("Saved rows:", len(output))
    print("Output:", OUTPUT_PATH)


if __name__ == "__main__":
    save_clean_dataset()


