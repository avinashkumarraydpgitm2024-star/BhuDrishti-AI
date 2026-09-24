def normalize_ndvi(ndvi):
    if ndvi is None:
        raise ValueError("NDVI value is required.")

    ndvi = float(ndvi)

    if not -1.0 <= ndvi <= 1.0:
        raise ValueError("NDVI must be between -1 and 1.")

    return {
        "ndvi": round(ndvi, 4)
    }


def calculate_ndvi(nir, red):
    nir = float(nir)
    red = float(red)

    denominator = nir + red

    if denominator == 0:
        raise ValueError("NDVI cannot be calculated when NIR + RED = 0.")

    ndvi = (nir - red) / denominator

    ndvi = max(-1.0, min(1.0, ndvi))

    return round(ndvi, 4)
