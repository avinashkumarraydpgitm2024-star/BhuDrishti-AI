from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.models.satellite_observation import SatelliteObservation
from backend.app.schemas.satellite_observation import (
    SatelliteObservationCreate,
)


def get_risk_zone_by_public_id(
    db: Session,
    public_id: str,
) -> RiskZone | None:
    statement = select(RiskZone).where(
        RiskZone.public_id == public_id
    )

    return db.scalar(statement)


def get_satellite_observation_by_scene_id(
    db: Session,
    scene_id: str,
) -> SatelliteObservation | None:
    normalized_scene_id = scene_id.strip()

    statement = select(SatelliteObservation).where(
        SatelliteObservation.scene_id == normalized_scene_id
    )

    return db.scalar(statement)


def get_satellite_observation_by_public_id(
    db: Session,
    public_id: str,
) -> SatelliteObservation | None:
    statement = select(SatelliteObservation).where(
        SatelliteObservation.public_id == public_id
    )

    return db.scalar(statement)


def create_satellite_observation(
    db: Session,
    observation_data: SatelliteObservationCreate,
) -> SatelliteObservation:
    scene_id = observation_data.scene_id.strip()

    existing = get_satellite_observation_by_scene_id(
        db=db,
        scene_id=scene_id,
    )

    if existing is not None:
        raise ValueError(
            "Satellite observation scene already exists."
        )

    risk_zone_id: int | None = None

    if observation_data.risk_zone_public_id:
        risk_zone = get_risk_zone_by_public_id(
            db=db,
            public_id=observation_data.risk_zone_public_id,
        )

        if risk_zone is None:
            raise ValueError(
                "Risk zone not found."
            )

        risk_zone_id = risk_zone.id

    observation = SatelliteObservation(
        risk_zone_id=risk_zone_id,
        provider=observation_data.provider.strip(),
        satellite_name=(
            observation_data.satellite_name.strip()
            if observation_data.satellite_name
            else None
        ),
        scene_id=scene_id,
        latitude=observation_data.latitude,
        longitude=observation_data.longitude,
        captured_at=observation_data.captured_at,
        cloud_cover_percent=observation_data.cloud_cover_percent,
        ndvi=observation_data.ndvi,
        ndwi=observation_data.ndwi,
        soil_moisture_index=(
            observation_data.soil_moisture_index
        ),
        surface_temperature_c=(
            observation_data.surface_temperature_c
        ),
        data_url=(
            str(observation_data.data_url)
            if observation_data.data_url
            else None
        ),
        thumbnail_url=(
            str(observation_data.thumbnail_url)
            if observation_data.thumbnail_url
            else None
        ),
    )

    db.add(observation)

    try:
        db.commit()
        db.refresh(observation)

    except Exception:
        db.rollback()
        raise

    return observation


def get_latest_satellite_observation_for_zone(
    db: Session,
    *,
    risk_zone_id: int,
) -> SatelliteObservation | None:
    statement = (
        select(SatelliteObservation)
        .where(
            SatelliteObservation.risk_zone_id == risk_zone_id
        )
        .order_by(
            SatelliteObservation.captured_at.desc()
        )
        .limit(1)
    )

    return db.scalar(statement)


def get_satellite_observation_history(
    db: Session,
    *,
    risk_zone_id: int,
    limit: int = 100,
) -> list[SatelliteObservation]:
    statement = (
        select(SatelliteObservation)
        .where(
            SatelliteObservation.risk_zone_id == risk_zone_id
        )
        .order_by(
            SatelliteObservation.captured_at.desc()
        )
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )