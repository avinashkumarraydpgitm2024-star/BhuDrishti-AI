from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SatelliteIndices:
    ndvi: float | None
    ndwi: float | None
    soil_moisture_index: float | None


def _safe_mean(values: np.ndarray) -> float | None:
    valid = values[np.isfinite(values)]

    if valid.size == 0:
        return None

    return float(np.mean(valid))


def calculate_ndvi(
    red: np.ndarray,
    nir: np.ndarray,
) -> float | None:
    red = red.astype(np.float32)
    nir = nir.astype(np.float32)

    denominator = nir + red

    with np.errstate(divide="ignore", invalid="ignore"):
        ndvi = np.where(
            denominator != 0,
            (nir - red) / denominator,
            np.nan,
        )

    return _safe_mean(ndvi)


def calculate_ndwi(
    green: np.ndarray,
    nir: np.ndarray,
) -> float | None:
    green = green.astype(np.float32)
    nir = nir.astype(np.float32)

    denominator = green + nir

    with np.errstate(divide="ignore", invalid="ignore"):
        ndwi = np.where(
            denominator != 0,
            (green - nir) / denominator,
            np.nan,
        )

    return _safe_mean(ndwi)


def calculate_soil_moisture_index(
    swir: np.ndarray,
    nir: np.ndarray,
) -> float | None:
    swir = swir.astype(np.float32)
    nir = nir.astype(np.float32)

    denominator = swir + nir

    with np.errstate(divide="ignore", invalid="ignore"):
        index = np.where(
            denominator != 0,
            (swir - nir) / denominator,
            np.nan,
        )

    mean_value = _safe_mean(index)

    if mean_value is None:
        return None

    return float(np.clip((mean_value + 1.0) / 2.0, 0.0, 1.0))


def calculate_satellite_indices(
    *,
    red: np.ndarray,
    green: np.ndarray,
    nir: np.ndarray,
    swir: np.ndarray,
    scl: np.ndarray | None = None,
) -> SatelliteIndices:
    if scl is not None:
        valid_mask = build_scl_valid_mask(scl)

        red = np.where(valid_mask, red, np.nan)
        green = np.where(valid_mask, green, np.nan)
        nir = np.where(valid_mask, nir, np.nan)
        swir = np.where(valid_mask, swir, np.nan)

    return SatelliteIndices(
        ndvi=calculate_ndvi(red, nir),
        ndwi=calculate_ndwi(green, nir),
        soil_moisture_index=calculate_soil_moisture_index(
            swir,
            nir,
        ),
    )
def build_scl_valid_mask(
    scl: np.ndarray,
) -> np.ndarray:
    """
    Build a quality mask from Sentinel-2 Scene Classification Layer.

    Valid classes:
    4  = Vegetation
    5  = Bare soils
    6  = Water
    7  = Unclassified
    """
    valid_classes = np.array(
        [4, 5, 6, 7],
        dtype=scl.dtype,
    )

    return np.isin(scl, valid_classes)

