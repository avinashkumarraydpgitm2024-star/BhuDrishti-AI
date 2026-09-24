from datetime import datetime


SUPPORTED_INCIDENT_TYPES = {
    "flood",
    "landslide",
    "road_blockage",
    "heavy_rain",
    "erosion"
}


def normalize_incident(incident):
    required_fields = [
        "latitude",
        "longitude",
        "incident_type",
        "timestamp"
    ]

    missing = [
        field for field in required_fields
        if field not in incident
    ]

    if missing:
        raise ValueError(
            f"Missing incident fields: {', '.join(missing)}"
        )

    incident_type = str(
        incident["incident_type"]
    ).lower().strip()

    if incident_type not in SUPPORTED_INCIDENT_TYPES:
        raise ValueError(
            f"Unsupported incident type: {incident_type}"
        )

    return {
        "latitude": float(incident["latitude"]),
        "longitude": float(incident["longitude"]),
        "incident_type": incident_type,
        "timestamp": str(incident["timestamp"])
    }


import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INCIDENT_DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "historical_incidents.json"
)


def load_historical_incidents():
    with open(
        INCIDENT_DATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        incidents = json.load(file)

    if not isinstance(incidents, list):
        raise ValueError(
            "Historical incident data must be a JSON list."
        )

    return incidents


import math


def haversine_km(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius_km * c


def count_nearby_incidents(latitude, longitude, radius_km=10):
    incidents = load_historical_incidents()

    count = 0

    for incident in incidents:
        distance = haversine_km(
            latitude,
            longitude,
            float(incident["latitude"]),
            float(incident["longitude"])
        )

        if distance <= radius_km:
            count += 1

    return count

USGS_LANDSLIDE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "usgs_landslides_clean.csv"
)


def load_usgs_landslides():
    import pandas as pd

    df = pd.read_csv(
        USGS_LANDSLIDE_PATH,
        low_memory=False
    )

    required_columns = {
        "latitude",
        "longitude",
        "date_min",
        "date_max",
        "Confidence",
        "landslide_category",
        "Inventory"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing USGS columns: {sorted(missing)}"
        )

    return df


def get_nearby_usgs_landslides(
    latitude,
    longitude,
    radius_km=10
):
    df = load_usgs_landslides()

    distances = df.apply(
        lambda row: haversine_km(
            float(latitude),
            float(longitude),
            float(row["latitude"]),
            float(row["longitude"])
        ),
        axis=1
    )

    nearby = df[
        distances <= float(radius_km)
    ].copy()

    nearby["distance_km"] = distances[
        distances <= float(radius_km)
    ]

    return nearby


from sklearn.neighbors import BallTree
import numpy as np


_USGS_DF_CACHE = None
_USGS_TREE_CACHE = None


def get_usgs_spatial_index():
    global _USGS_DF_CACHE, _USGS_TREE_CACHE

    if _USGS_DF_CACHE is None or _USGS_TREE_CACHE is None:
        df = load_usgs_landslides().copy()

        coordinates_radians = np.radians(
            df[["latitude", "longitude"]].to_numpy(
                dtype=float
            )
        )

        tree = BallTree(
            coordinates_radians,
            metric="haversine"
        )

        _USGS_DF_CACHE = df
        _USGS_TREE_CACHE = tree

    return _USGS_DF_CACHE, _USGS_TREE_CACHE


def get_nearby_usgs_landslides_fast(
    latitude,
    longitude,
    radius_km=10
):
    earth_radius_km = 6371.0

    df, tree = get_usgs_spatial_index()

    query_point = np.radians(
        [[float(latitude), float(longitude)]]
    )

    radius_radians = (
        float(radius_km) / earth_radius_km
    )

    indices, distances = tree.query_radius(
        query_point,
        r=radius_radians,
        return_distance=True,
        sort_results=True
    )

    nearby = df.iloc[
        indices[0]
    ].copy()

    nearby["distance_km"] = (
        distances[0] * earth_radius_km
    )

    return nearby


def summarize_historical_landslide_evidence(
    latitude,
    longitude,
    radius_km=10
):
    nearby = get_nearby_usgs_landslides_fast(
        latitude,
        longitude,
        radius_km
    ).copy()

    import pandas as pd

    date_min = pd.to_datetime(
        nearby["date_min"],
        errors="coerce",
        format="mixed"
    )

    dated_mask = date_min.notna()

    return {
        "total_records": int(len(nearby)),
        "dated_records": int(dated_mask.sum()),
        "undated_records": int((~dated_mask).sum()),
        "unique_inventories": int(
            nearby["Inventory"].nunique()
        )
    }


def summarize_usgs_confidence(
    latitude,
    longitude,
    radius_km=10
):
    nearby = get_nearby_usgs_landslides_fast(
        latitude,
        longitude,
        radius_km
    )

    counts = (
        nearby["Confidence"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    return {
        int(key): int(value)
        for key, value in counts.items()
    }


def build_usgs_historical_evidence(
    latitude,
    longitude,
    radius_km=10
):
    summary = summarize_historical_landslide_evidence(
        latitude,
        longitude,
        radius_km
    )

    confidence = summarize_usgs_confidence(
        latitude,
        longitude,
        radius_km
    )

    return {
        "source": "USGS",
        "coverage": "United States only",
        "radius_km": float(radius_km),
        "total_records": summary["total_records"],
        "dated_records": summary["dated_records"],
        "undated_records": summary["undated_records"],
        "unique_inventories": summary["unique_inventories"],
        "confidence_counts": confidence
    }


def build_usgs_distance_band_features(
    latitude,
    longitude
):
    nearby_10km = get_nearby_usgs_landslides_fast(
        latitude,
        longitude,
        10
    )

    distances = nearby_10km["distance_km"]

    return {
        "within_1km": int((distances <= 1).sum()),
        "within_5km": int((distances <= 5).sum()),
        "within_10km": int((distances <= 10).sum())
    }


def build_usgs_log_distance_features(
    latitude,
    longitude
):
    bands = build_usgs_distance_band_features(
        latitude,
        longitude
    )

    return {
        "log_within_1km": float(
            np.log1p(bands["within_1km"])
        ),
        "log_within_5km": float(
            np.log1p(bands["within_5km"])
        ),
        "log_within_10km": float(
            np.log1p(bands["within_10km"])
        )
    }


def build_usgs_spatial_history_features(
    latitude,
    longitude
):
    raw = build_usgs_distance_band_features(
        latitude,
        longitude
    )

    log_features = build_usgs_log_distance_features(
        latitude,
        longitude
    )

    return {
        **raw,
        **log_features
    }


def is_usgs_coverage_available(
    latitude,
    longitude
):
    lat = float(latitude)
    lon = float(longitude)

    # Approximate geographic bounds of the current
    # USGS United States landslide dataset.
    return (
        17.0 <= lat <= 71.0
        and -165.0 <= lon <= -65.0
    )
