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
