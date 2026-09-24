import requests
from datetime import datetime, timedelta, timezone

from backend.data_pipeline.satellite_config import (
    MAX_CLOUD_COVER,
    LOOKBACK_DAYS
)


STAC_SEARCH_URL = (
    "https://stac.dataspace.copernicus.eu/v1/search"
)

SENTINEL_COLLECTION = "sentinel-2-l2a"


def search_sentinel_scenes(latitude, longitude):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=LOOKBACK_DAYS)

    payload = {
        "collections": [SENTINEL_COLLECTION],
        "bbox": [
            longitude - 0.01,
            latitude - 0.01,
            longitude + 0.01,
            latitude + 0.01
        ],
        "datetime": (
            f"{start_time.isoformat()}/"
            f"{end_time.isoformat()}"
        ),
        "limit": 10,
        "query": {
            "eo:cloud_cover": {
                "lte": MAX_CLOUD_COVER
            }
        }
    }

    response = requests.post(
        STAC_SEARCH_URL,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data.get("features", [])


def get_https_asset_url(scene, asset_key):
    assets = scene.get("assets", {})

    if asset_key not in assets:
        raise ValueError(
            f"Asset '{asset_key}' not found in Sentinel-2 scene."
        )

    asset = assets[asset_key]

    alternate = asset.get("alternate", {})
    https_info = alternate.get("https", {})
    https_url = https_info.get("href")

    if not https_url:
        raise ValueError(
            f"HTTPS URL not available for asset '{asset_key}'."
        )

    return {
        "asset_key": asset_key,
        "url": https_url,
        "auth_required": "oidc" in https_info.get("auth:refs", [])
    }
