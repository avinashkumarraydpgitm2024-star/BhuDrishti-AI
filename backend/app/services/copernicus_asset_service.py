from __future__ import annotations

from typing import Any


REQUIRED_BANDS = (
    "B03_10m",
    "B04_10m",
    "B08_10m",
    "B11_20m",
    "SCL_20m",
)


def extract_required_assets(
    assets: dict[str, Any],
) -> dict[str, str]:
    """Return the Sentinel-2 assets required by BhuDrishti."""

    missing = [
        name
        for name in REQUIRED_BANDS
        if name not in assets
    ]

    if missing:
        raise ValueError(
            f"Required Sentinel-2 assets missing: {', '.join(missing)}"
        )

    return {
        name: str(assets[name].href)
        for name in REQUIRED_BANDS
    }
from urllib.parse import urlparse


def validate_satellite_asset_url(
    asset_url: str,
) -> str:
    """Validate and normalize a Copernicus satellite asset URL."""

    url = asset_url.strip()

    if not url:
        raise ValueError("Satellite asset URL cannot be empty.")

    parsed = urlparse(url)

    if parsed.scheme not in {"s3", "https"}:
        raise ValueError(
            f"Unsupported satellite asset scheme: {parsed.scheme}"
        )

    if parsed.scheme == "s3" and parsed.netloc != "eodata":
        raise ValueError(
            "Only the Copernicus eodata S3 bucket is supported."
        )

    if not parsed.path:
        raise ValueError(
            "Satellite asset URL must contain an object path."
        )

    return url


def is_s3_asset(asset_url: str) -> bool:
    return urlparse(asset_url.strip()).scheme == "s3"


def is_https_asset(asset_url: str) -> bool:
    return urlparse(asset_url.strip()).scheme == "https"

