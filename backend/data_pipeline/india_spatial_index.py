from pathlib import Path
from functools import lru_cache

import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "india_historical_incidents_clean.csv"

EARTH_RADIUS_KM = 6371.0088


@lru_cache(maxsize=1)
def load_india_landslide_inventory():
    df = pd.read_csv(DATA_PATH)

    valid_df = df[
        df["coordinate_valid"].eq(True)
        & df["latitude_clean"].notna()
        & df["longitude_clean"].notna()
    ].copy()

    coordinates_radians = np.radians(
        valid_df[["latitude_clean", "longitude_clean"]].to_numpy(dtype=float)
    )

    tree = BallTree(coordinates_radians, metric="haversine")

    return valid_df.reset_index(drop=True), tree


if __name__ == "__main__":
    inventory, spatial_tree = load_india_landslide_inventory()

    print(f"Dataset: {DATA_PATH}")
    print(f"Valid inventory records: {len(inventory):,}")
    print("India GSI BallTree spatial index ready.")


def find_nearby_landslides(latitude, longitude, radius_km=10.0):
    inventory, tree = load_india_landslide_inventory()

    query_point = np.radians([[float(latitude), float(longitude)]])
    radius_radians = float(radius_km) / EARTH_RADIUS_KM

    indices, distances = tree.query_radius(
        query_point,
        r=radius_radians,
        return_distance=True,
        sort_results=True,
    )

    nearby = inventory.iloc[indices[0]].copy()
    nearby["distance_km"] = distances[0] * EARTH_RADIUS_KM

    return nearby.reset_index(drop=True)


def get_spatial_history_summary(latitude, longitude):
    within_1km = find_nearby_landslides(latitude, longitude, 1.0)
    within_5km = find_nearby_landslides(latitude, longitude, 5.0)
    within_10km = find_nearby_landslides(latitude, longitude, 10.0)

    return {
        "gsi_inventory_within_1km": len(within_1km),
        "gsi_inventory_within_5km": len(within_5km),
        "gsi_inventory_within_10km": len(within_10km),
    }




def get_nearest_landslide(latitude, longitude):
    inventory, tree = load_india_landslide_inventory()

    query_point = np.radians([[float(latitude), float(longitude)]])

    distances, indices = tree.query(
        query_point,
        k=1,
        return_distance=True,
    )

    row = inventory.iloc[int(indices[0][0])]

    return {
        "serial_no": int(row["serial_no"]),
        "state": row["state_normalized"],
        "district": row["district"],
        "movement_type": row["movement_type_normalized"],
        "material": row["material_normalized"],
        "distance_km": round(float(distances[0][0] * EARTH_RADIUS_KM), 3),
    }


def get_india_spatial_evidence(latitude, longitude):
    latitude, longitude = validate_coordinates(latitude, longitude)
    summary = get_spatial_history_summary(latitude, longitude)
    nearest = get_nearest_landslide(latitude, longitude)

    return {
        "source": "GSI National Landslide Inventory",
        "evidence_type": "historical_inventory_proximity",
        **summary,
        "nearest_inventory_record": nearest,
        "interpretation_note": (
            "Inventory proximity is supporting historical evidence, "
            "not a calibrated landslide probability."
        ),
    }


def validate_coordinates(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)

    if not -90.0 <= latitude <= 90.0:
        raise ValueError("Latitude must be between -90 and 90.")

    if not -180.0 <= longitude <= 180.0:
        raise ValueError("Longitude must be between -180 and 180.")

    return latitude, longitude

