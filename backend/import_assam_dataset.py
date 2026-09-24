from pathlib import Path

import pandas as pd
from sqlalchemy import text

from backend.app.core.database import engine


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    BASE_DIR
    / "data"
    / "synthetic"
)

TABLE_NAME = "assam_landslide_dataset"

# SQLite ke liye safe batch size
BATCH_SIZE = 500


# ============================================================
# EXPECTED ASSAM DATASET COLUMNS
# ============================================================

EXPECTED_COLUMNS = [
    "record_id",
    "district",
    "latitude",
    "longitude",
    "elevation_m",
    "slope_deg",
    "rainfall_24h_mm",
    "rainfall_72h_mm",
    "rainfall_7d_mm",
    "soil_moisture_index",
    "soil_type",
    "geology",
    "land_cover",
    "ndvi",
    "road_distance_km",
    "river_distance_km",
    "road_cutting",
    "deforestation_index",
    "landslide_occurrence",
    "risk_score",
    "risk_level",
]


# ============================================================
# FIND ASSAM DATASET AUTOMATICALLY
# ============================================================

def find_assam_dataset() -> Path:
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Data directory not found:\n{DATA_DIR}"
        )

    csv_files = sorted(
        DATA_DIR.glob("*.csv")
    )

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in:\n{DATA_DIR}"
        )

    matches: list[Path] = []

    print("Searching Assam dataset...")
    print()

    for csv_path in csv_files:

        try:
            columns = pd.read_csv(
                csv_path,
                nrows=0,
            ).columns.tolist()

        except Exception as exc:
            print(
                f"Skipping unreadable CSV: "
                f"{csv_path.name}"
            )
            print(f"Reason: {exc}")
            print()
            continue

        missing = [
            column
            for column in EXPECTED_COLUMNS
            if column not in columns
        ]

        if not missing:
            matches.append(csv_path)

    if not matches:
        print(
            "No CSV with the expected Assam "
            "dataset columns was found."
        )

        print()
        print("CSV files checked:")

        for csv_path in csv_files:
            print(
                f"- {csv_path.name}"
            )

        raise FileNotFoundError(
            "Assam 21-column dataset CSV "
            "could not be identified."
        )

    if len(matches) > 1:

        print(
            "Multiple matching CSV files found:"
        )

        for csv_path in matches:
            print(
                f"- {csv_path.name}"
            )

        # Prefer the largest matching CSV.
        selected = max(
            matches,
            key=lambda path: path.stat().st_size,
        )

        print()
        print(
            "Selecting largest matching dataset:"
        )
        print(
            selected.name
        )

        return selected

    return matches[0]


# ============================================================
# VALIDATION
# ============================================================

def validate_dataset(
    df: pd.DataFrame,
) -> pd.DataFrame:

    print(
        f"Rows loaded: {len(df):,}"
    )

    if df.empty:
        raise ValueError(
            "Dataset is empty."
        )

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing columns:\n"
            + "\n".join(
                f"- {column}"
                for column in missing_columns
            )
        )

    # Only use expected 21 columns.
    df = df[
        EXPECTED_COLUMNS
    ].copy()

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    missing_values = int(
        df.isna().sum().sum()
    )

    if missing_values:
        raise ValueError(
            f"Dataset contains "
            f"{missing_values:,} missing values."
        )

    # --------------------------------------------------------
    # Duplicate record IDs
    # --------------------------------------------------------

    duplicate_ids = int(
        df["record_id"]
        .duplicated()
        .sum()
    )

    if duplicate_ids:
        raise ValueError(
            f"Duplicate record_id values: "
            f"{duplicate_ids:,}"
        )

    # --------------------------------------------------------
    # Numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "record_id",
        "latitude",
        "longitude",
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
        "landslide_occurrence",
        "risk_score",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="raise",
        )

    # --------------------------------------------------------
    # Integer columns
    # --------------------------------------------------------

    df["record_id"] = (
        df["record_id"]
        .astype(int)
    )

    df["road_cutting"] = (
        df["road_cutting"]
        .astype(int)
    )

    df["landslide_occurrence"] = (
        df["landslide_occurrence"]
        .astype(int)
    )

    # --------------------------------------------------------
    # String columns
    # --------------------------------------------------------

    string_columns = [
        "district",
        "soil_type",
        "geology",
        "land_cover",
        "risk_level",
    ]

    for column in string_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    # --------------------------------------------------------
    # Binary validation
    # --------------------------------------------------------

    occurrence_values = set(
        df[
            "landslide_occurrence"
        ].unique()
    )

    if not occurrence_values.issubset(
        {0, 1}
    ):
        raise ValueError(
            "landslide_occurrence must "
            "contain only 0 or 1."
        )

    road_cutting_values = set(
        df[
            "road_cutting"
        ].unique()
    )

    if not road_cutting_values.issubset(
        {0, 1}
    ):
        raise ValueError(
            "road_cutting must "
            "contain only 0 or 1."
        )

    # --------------------------------------------------------
    # Coordinate validation
    # --------------------------------------------------------

    invalid_latitude = (
        (df["latitude"] < -90)
        | (df["latitude"] > 90)
    )

    invalid_longitude = (
        (df["longitude"] < -180)
        | (df["longitude"] > 180)
    )

    if invalid_latitude.any():
        raise ValueError(
            "Invalid latitude value found."
        )

    if invalid_longitude.any():
        raise ValueError(
            "Invalid longitude value found."
        )

    print(
        "Dataset validation: PASS"
    )

    return df


# ============================================================
# DATABASE IMPORT
# ============================================================

def import_dataset(
    df: pd.DataFrame,
) -> None:

    total_rows = len(df)

    print()
    print(
        f"Preparing to import "
        f"{total_rows:,} records..."
    )

    print(
        f"Batch size: {BATCH_SIZE}"
    )

    print()

    # One transaction for complete import.
    with engine.begin() as connection:

        print(
            "Clearing existing "
            "Assam dataset records..."
        )

        connection.execute(
            text(
                f"""
                DELETE FROM {TABLE_NAME}
                """
            )
        )

        print(
            "Existing records cleared."
        )

        print()

        inserted = 0

        for start in range(
            0,
            total_rows,
            BATCH_SIZE,
        ):

            end = min(
                start + BATCH_SIZE,
                total_rows,
            )

            batch = df.iloc[
                start:end
            ]

            records = (
                batch
                .to_dict(
                    orient="records"
                )
            )

            connection.execute(
                text(
                    f"""
                    INSERT INTO {TABLE_NAME} (
                        record_id,
                        district,
                        latitude,
                        longitude,
                        elevation_m,
                        slope_deg,
                        rainfall_24h_mm,
                        rainfall_72h_mm,
                        rainfall_7d_mm,
                        soil_moisture_index,
                        soil_type,
                        geology,
                        land_cover,
                        ndvi,
                        road_distance_km,
                        river_distance_km,
                        road_cutting,
                        deforestation_index,
                        landslide_occurrence,
                        risk_score,
                        risk_level
                    )
                    VALUES (
                        :record_id,
                        :district,
                        :latitude,
                        :longitude,
                        :elevation_m,
                        :slope_deg,
                        :rainfall_24h_mm,
                        :rainfall_72h_mm,
                        :rainfall_7d_mm,
                        :soil_moisture_index,
                        :soil_type,
                        :geology,
                        :land_cover,
                        :ndvi,
                        :road_distance_km,
                        :river_distance_km,
                        :road_cutting,
                        :deforestation_index,
                        :landslide_occurrence,
                        :risk_score,
                        :risk_level
                    )
                    """
                ),
                records,
            )

            inserted += len(
                batch
            )

            percentage = (
                inserted
                / total_rows
                * 100
            )

            print(
                f"Imported "
                f"{inserted:,}/"
                f"{total_rows:,} "
                f"({percentage:.1f}%)"
            )

        # ----------------------------------------------------
        # Verify before committing
        # ----------------------------------------------------

        db_count = connection.execute(
            text(
                f"""
                SELECT COUNT(*)
                FROM {TABLE_NAME}
                """
            )
        ).scalar_one()

        print()
        print(
            f"Database count before commit: "
            f"{db_count:,}"
        )

        if db_count != total_rows:
            raise RuntimeError(
                "Import verification failed. "
                f"Expected {total_rows:,}, "
                f"found {db_count:,}."
            )


# ============================================================
# FINAL DATABASE VERIFICATION
# ============================================================

def verify_database(
    expected_count: int,
) -> None:

    with engine.connect() as connection:

        actual_count = connection.execute(
            text(
                f"""
                SELECT COUNT(*)
                FROM {TABLE_NAME}
                """
            )
        ).scalar_one()

    print()
    print("=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)
    print()

    print(
        f"Expected records : "
        f"{expected_count:,}"
    )

    print(
        f"Database records : "
        f"{actual_count:,}"
    )

    if actual_count != expected_count:
        raise RuntimeError(
            "FINAL VERIFICATION FAILED."
        )

    print()
    print(
        "STATUS: SUCCESS"
    )
    print(
        "100% Assam dataset imported."
    )
    print()


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print()
    print("=" * 60)
    print("ASSAM LANDSLIDE DATASET IMPORT")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Find actual CSV automatically
    # --------------------------------------------------------

    dataset_path = (
        find_assam_dataset()
    )

    print(
        "Dataset selected:"
    )

    print(
        dataset_path
    )

    print()

    # --------------------------------------------------------
    # Load CSV
    # --------------------------------------------------------

    df = pd.read_csv(
        dataset_path
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    df = validate_dataset(
        df
    )

    print()

    # --------------------------------------------------------
    # Dataset information
    # --------------------------------------------------------

    print(
        "Risk levels:"
    )

    print(
        df[
            "risk_level"
        ]
        .value_counts()
        .to_string()
    )

    print()

    print(
        "Landslide occurrence:"
    )

    print(
        df[
            "landslide_occurrence"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print()

    # --------------------------------------------------------
    # Import
    # --------------------------------------------------------

    import_dataset(
        df
    )

    # --------------------------------------------------------
    # Final verification
    # --------------------------------------------------------

    verify_database(
        expected_count=len(df)
    )


if __name__ == "__main__":
    main()