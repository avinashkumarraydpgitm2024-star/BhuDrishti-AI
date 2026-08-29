from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from pystac_client import Client

from backend.app.core.config import settings


SENTINEL_2_L2A_COLLECTION = "sentinel-2-l2a"


class CopernicusSTACService:
    """Read-only Sentinel-2 discovery service backed by Copernicus STAC."""

    def __init__(
        self,
        stac_url: str | None = None,
    ) -> None:
        self.stac_url = (
            stac_url
            or settings.satellite_stac_url
        )

    def _catalog(self) -> Client:
        return Client.open(self.stac_url)

    def search_sentinel2(
        self,
        *,
        latitude: float,
        longitude: float,
        days: int | None = None,
        max_cloud_cover: float | None = None,
        max_items: int = 20,
    ) -> list[dict[str, Any]]:
        search_days = (
            days
            if days is not None
            else settings.satellite_search_days
        )

        cloud_limit = (
            max_cloud_cover
            if max_cloud_cover is not None
            else settings.satellite_default_cloud_cover_max
        )

        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")

        if search_days < 1:
            raise ValueError("Search days must be at least 1.")

        if not 0 <= cloud_limit <= 100:
            raise ValueError(
                "Maximum cloud cover must be between 0 and 100."
            )

        if max_items < 1:
            raise ValueError("max_items must be at least 1.")

        now = datetime.now(timezone.utc)
        start = now - timedelta(days=search_days)

        bbox_delta = 0.1

        bbox = [
            longitude - bbox_delta,
            latitude - bbox_delta,
            longitude + bbox_delta,
            latitude + bbox_delta,
        ]

        catalog = self._catalog()

        search = catalog.search(
            collections=[SENTINEL_2_L2A_COLLECTION],
            bbox=bbox,
            datetime=(
                f"{start.isoformat()}/"
                f"{now.isoformat()}"
            ),
            query={
                "eo:cloud_cover": {
                    "lte": cloud_limit,
                }
            },
            max_items=max_items,
        )

        results: list[dict[str, Any]] = []

        for item in search.items():
            results.append(
                {
                    "scene_id": item.id,
                    "captured_at": item.datetime,
                    "cloud_cover_percent": item.properties.get(
                        "eo:cloud_cover"
                    ),
                    "latitude": item.geometry
                    and item.geometry.get("coordinates"),
                    "bbox": item.bbox,
                    "collection": item.collection_id,
                    "assets": {
                        key: asset.href
                        for key, asset in item.assets.items()
                    },
                }
            )

        return results

    def find_best_scene(
        self,
        *,
        latitude: float,
        longitude: float,
        days: int | None = None,
        max_cloud_cover: float | None = None,
    ) -> dict[str, Any] | None:
        scenes = self.search_sentinel2(
            latitude=latitude,
            longitude=longitude,
            days=days,
            max_cloud_cover=max_cloud_cover,
            max_items=50,
        )

        if not scenes:
            return None

        scenes.sort(
            key=lambda scene: (
                scene["cloud_cover_percent"]
                if scene["cloud_cover_percent"] is not None
                else 100.0,
                -(
                    scene["captured_at"].timestamp()
                    if scene["captured_at"] is not None
                    else 0.0
                ),
            )
        )

        return scenes[0]

