from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio


def read_single_band(
    path: str | Path,
) -> np.ndarray:
    """Read a single-band raster as a float32 NumPy array."""

    raster_path = Path(path)

    if not raster_path.exists():
        raise FileNotFoundError(
            f"Raster file not found: {raster_path}"
        )

    with rasterio.open(raster_path) as dataset:
        if dataset.count != 1:
            raise ValueError(
                f"Expected a single-band raster, found {dataset.count} bands."
            )

        data = dataset.read(1)

        if dataset.nodata is not None:
            data = np.where(
                data == dataset.nodata,
                np.nan,
                data,
            )

        return data.astype(np.float32)


def get_raster_metadata(
    path: str | Path,
) -> dict[str, object]:
    """Return essential geospatial metadata for a raster."""

    raster_path = Path(path)

    if not raster_path.exists():
        raise FileNotFoundError(
            f"Raster file not found: {raster_path}"
        )

    with rasterio.open(raster_path) as dataset:
        return {
            "width": dataset.width,
            "height": dataset.height,
            "count": dataset.count,
            "dtype": dataset.dtypes[0],
            "crs": str(dataset.crs)
            if dataset.crs
            else None,
            "transform": tuple(dataset.transform),
            "nodata": dataset.nodata,
            "bounds": (
                dataset.bounds.left,
                dataset.bounds.bottom,
                dataset.bounds.right,
                dataset.bounds.top,
            ),
        }
