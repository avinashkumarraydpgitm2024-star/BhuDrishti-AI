import numpy as np

from backend.app.services.satellite_band_processing_service import (
    build_scl_valid_mask,
    calculate_satellite_indices,
)


def test_scl_mask_rejects_cloud_pixels():
    scl = np.array(
        [[4, 5, 8, 9, 10, 11]],
        dtype=np.uint8,
    )

    mask = build_scl_valid_mask(scl)

    assert mask.tolist()[0] == [
        True,
        True,
        False,
        False,
        False,
        False,
    ]


def test_satellite_indices_use_only_valid_scl_pixels():
    red = np.array(
        [[0.2, 0.9]],
        dtype=np.float32,
    )
    green = np.array(
        [[0.3, 0.8]],
        dtype=np.float32,
    )
    nir = np.array(
        [[0.6, 0.1]],
        dtype=np.float32,
    )
    swir = np.array(
        [[0.4, 0.2]],
        dtype=np.float32,
    )
    scl = np.array(
        [[4, 9]],
        dtype=np.uint8,
    )

    result = calculate_satellite_indices(
        red=red,
        green=green,
        nir=nir,
        swir=swir,
        scl=scl,
    )

    assert result.ndvi is not None
    assert result.ndwi is not None
    assert result.soil_moisture_index is not None

    assert abs(result.ndvi - 0.5) < 1e-5
    assert abs(result.ndwi + (1 / 3)) < 1e-5
    assert abs(result.soil_moisture_index - 0.4) < 1e-5
