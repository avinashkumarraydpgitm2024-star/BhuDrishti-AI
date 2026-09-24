import requests


ELEVATION_URL = "https://api.open-meteo.com/v1/elevation"


def get_elevation(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude
    }

    response = requests.get(
        ELEVATION_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    elevations = data.get("elevation")

    if not elevations:
        raise ValueError("Elevation data not available.")

    return {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "elevation_m": float(elevations[0])
    }
