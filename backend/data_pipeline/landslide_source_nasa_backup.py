import requests


NASA_COOLR_URL = (
    "https://gis.earthdata.nasa.gov/gis05/rest/services/"
    "Landslides/COOLR_Events_Points/MapServer/0/query"
)


def fetch_landslide_records(limit=100):
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit
    }

    response = requests.get(
        NASA_COOLR_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(
            f"NASA COOLR API error: {data['error']}"
        )

    return data.get("features", [])

