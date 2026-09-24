from math import cos, radians
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


ASSAM_DATASET_TABLE = "assam_landslide_dataset"


def get_nearest_assam_record(
    db: Session,
    *,
    latitude: float,
    longitude: float,
) -> dict[str, Any] | None:
    """
    Find the geographically nearest record from the
    imported Assam landslide dataset.

    The SQLite query first narrows the search to a
    small bounding box and then calculates an
    approximate squared geographic distance.
    """

    latitude = float(latitude)
    longitude = float(longitude)

    # Small search window around requested location.
    # Approximately ~5-6 km depending on latitude.
    lat_delta = 0.05

    cos_latitude = max(
        0.1,
        abs(cos(radians(latitude))),
    )

    lon_delta = 0.05 / cos_latitude

    min_latitude = latitude - lat_delta
    max_latitude = latitude + lat_delta

    min_longitude = longitude - lon_delta
    max_longitude = longitude + lon_delta

    statement = text(
        f"""
        SELECT
            record_id,
            district,
            latitude,
            longitude,
            elevation_m,
            slope_deg,
            rainfall_24h_mm,
            rainfall_72h_mm,
            rainfall_7d_mm,
            soil_moisture_index,
            soil_type,
            geology,
            land_cover,
            ndvi,
            road_distance_km,
            river_distance_km,
            road_cutting,
            deforestation_index,
            landslide_occurrence,
            risk_score,
            risk_level
        FROM {ASSAM_DATASET_TABLE}
        WHERE
            latitude BETWEEN :min_latitude
            AND :max_latitude
            AND longitude BETWEEN :min_longitude
            AND :max_longitude
        ORDER BY
            (
                (latitude - :latitude)
                * (latitude - :latitude)
                +
                (longitude - :longitude)
                * (longitude - :longitude)
            ) ASC
        LIMIT 1
        """
    )

    row = db.execute(
        statement,
        {
            "latitude": latitude,
            "longitude": longitude,
            "min_latitude": min_latitude,
            "max_latitude": max_latitude,
            "min_longitude": min_longitude,
            "max_longitude": max_longitude,
        },
    ).mappings().first()

    if row is None:
        return None

    return dict(row)


def build_assam_ml_features(
    record: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert a database dataset record into the exact
    feature structure expected by predict_assam_landslide().
    """

    return {
        "elevation_m": float(
            record["elevation_m"]
        ),
        "slope_deg": float(
            record["slope_deg"]
        ),
        "rainfall_24h_mm": float(
            record["rainfall_24h_mm"]
        ),
        "rainfall_72h_mm": float(
            record["rainfall_72h_mm"]
        ),
        "rainfall_7d_mm": float(
            record["rainfall_7d_mm"]
        ),
        "soil_moisture_index": float(
            record["soil_moisture_index"]
        ),
        "ndvi": float(
            record["ndvi"]
        ),
        "road_distance_km": float(
            record["road_distance_km"]
        ),
        "river_distance_km": float(
            record["river_distance_km"]
        ),
        "road_cutting": int(
            record["road_cutting"]
        ),
        "deforestation_index": float(
            record["deforestation_index"]
        ),
        "soil_type": str(
            record["soil_type"]
        ),
        "geology": str(
            record["geology"]
        ),
        "land_cover": str(
            record["land_cover"]
        ),
    }
