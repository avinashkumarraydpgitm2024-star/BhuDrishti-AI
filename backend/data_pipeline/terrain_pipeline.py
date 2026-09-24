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

def get_nearby_elevations(latitude, longitude, offset=0.001):
    points = {
        "center": (latitude, longitude),
        "north": (latitude + offset, longitude),
        "south": (latitude - offset, longitude),
        "east": (latitude, longitude + offset),
        "west": (latitude, longitude - offset)
    }

    results = {}

    for name, (lat, lon) in points.items():
        results[name] = get_elevation(lat, lon)

    return results

import math


def calculate_slope(latitude, longitude, offset=0.001):
    elevations = get_nearby_elevations(
        latitude,
        longitude,
        offset
    )

    north = elevations["north"]["elevation_m"]
    south = elevations["south"]["elevation_m"]
    east = elevations["east"]["elevation_m"]
    west = elevations["west"]["elevation_m"]

    lat_distance_m = 2 * offset * 111320

    lon_distance_m = (
        2
        * offset
        * 111320
        * math.cos(math.radians(latitude))
    )

    dz_dy = (north - south) / lat_distance_m
    dz_dx = (east - west) / lon_distance_m

    gradient = math.sqrt(
        (dz_dx ** 2) + (dz_dy ** 2)
    )

    slope_degrees = math.degrees(
        math.atan(gradient)
    )

    return {
        "slope_degrees": round(slope_degrees, 2),
        "elevations": elevations
    }
