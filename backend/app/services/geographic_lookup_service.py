from functools import lru_cache
from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

GSI_DATA_FILE = (
    PROJECT_ROOT
    / "backend"
    / "data"
    / "india_historical_incidents_clean.csv"
)


def _normalize_text(value: str) -> str:
    value = str(value or "").casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


@lru_cache(maxsize=1)
def _load_location_inventory() -> pd.DataFrame:
    if not GSI_DATA_FILE.exists():
        raise RuntimeError(
            "GSI historical inventory file not found."
        )

    df = pd.read_csv(GSI_DATA_FILE)

    required_columns = {
        "state_normalized",
        "district",
        "slide_name",
        "nh_sh_location",
        "latitude_clean",
        "longitude_clean",
        "coordinate_valid",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise RuntimeError(
            f"GSI location columns missing: {sorted(missing)}"
        )

    df = df[
        df["coordinate_valid"].eq(True)
        & df["latitude_clean"].notna()
        & df["longitude_clean"].notna()
    ].copy()

    for column in (
        "state_normalized",
        "district",
        "slide_name",
        "nh_sh_location",
    ):
        df[f"{column}_search"] = (
            df[column]
            .fillna("")
            .astype(str)
            .map(_normalize_text)
        )

    return df.reset_index(drop=True)


def find_location_records(
    location_name: str,
    *,
    limit: int = 20,
) -> list[dict]:
    query = _normalize_text(location_name)

    if len(query) < 3:
        return []

    df = _load_location_inventory()

    mask = (
        df["state_normalized_search"].str.contains(
            query,
            regex=False,
        )
        | df["district_search"].str.contains(
            query,
            regex=False,
        )
        | df["slide_name_search"].str.contains(
            query,
            regex=False,
        )
        | df["nh_sh_location_search"].str.contains(
            query,
            regex=False,
        )
    )

    matches = df.loc[mask].head(limit)

    return [
        {
            "state": row["state_normalized"],
            "district": row["district"],
            "slide_name": row["slide_name"],
            "location": row["nh_sh_location"],
            "latitude": float(row["latitude_clean"]),
            "longitude": float(row["longitude_clean"]),
        }
        for _, row in matches.iterrows()
    ]
