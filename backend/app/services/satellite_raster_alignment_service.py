from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


def resample_to_reference(
    source_path: str | Path,
    reference_path: str | Path,
    *,
    resampling: Resampling = Resampling.bilinear,
) -> np.ndarray:
    source_path = Path(source_path)
    reference_path = Path(reference_path)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source raster not found: {source_path}"
        )

    if not reference_path.exists():
        raise FileNotFoundError(
            f"Reference raster not found: {reference_path}"
        )

    with rasterio.open(source_path) as source:
        with rasterio.open(reference_path) as reference:
            destination = np.full(
                (reference.height, reference.width),
                np.nan,
                dtype=np.float32,
            )

            reproject(
                source=source.read(1),
                destination=destination,
                src_transform=source.transform,
                src_crs=source.crs,
                dst_transform=reference.transform,
                dst_crs=reference.crs,
                resampling=resampling,
                src_nodata=source.nodata,
                dst_nodata=np.nan,
            )

            return destination


def get_common_grid(
    reference_path: str | Path,
) -> dict[str, object]:
    reference_path = Path(reference_path)

    if not reference_path.exists():
        raise FileNotFoundError(
            f"Reference raster not found: {reference_path}"
        )

    with rasterio.open(reference_path) as dataset:
        return {
            "width": dataset.width,
            "height": dataset.height,
            "crs": str(dataset.crs) if dataset.crs else None,
            "transform": tuple(dataset.transform),
            "bounds": (
                dataset.bounds.left,
                dataset.bounds.bottom,
                dataset.bounds.right,
                dataset.bounds.top,
            ),
        }
