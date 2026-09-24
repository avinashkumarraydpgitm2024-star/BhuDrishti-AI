import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDIA_INCIDENT_DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "india_historical_incidents.csv"
)


def get_india_incident_data_path():
    return INDIA_INCIDENT_DATA_PATH
import requests


GSI_API_BASE_URL = (
    "https://bhusanket.gsi.gov.in/WebAPI_v2"
)


def fetch_gsi_landslide_count():
    url = (
        f"{GSI_API_BASE_URL}"
        "/Landslide/countGeojson"
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://bhusanket.gsi.gov.in/",
        "Origin": "https://bhusanket.gsi.gov.in"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("statusCode") != 200:
        raise RuntimeError(
            data.get(
                "statusMessage",
                "GSI API request failed"
            )
        )

    return int(
        data["result"][0]["count"]
    )
