from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.landslide_event import LandslideEvent
from backend.data_pipeline.india_spatial_index import (
    get_india_spatial_evidence,
)


def get_historical_event_count(
    db: Session,
    *,
    risk_zone_id: int,
    years: int = 10,
) -> int:
    since = datetime.now(timezone.utc) - timedelta(
        days=365 * years
    )

    statement = select(
        func.count(LandslideEvent.id)
    ).where(
        LandslideEvent.risk_zone_id == risk_zone_id,
        LandslideEvent.occurred_at >= since,
    )

    count = db.scalar(statement)

    return int(count or 0)


def get_recent_landslide_events(
    db: Session,
    *,
    risk_zone_id: int,
    limit: int = 20,
) -> list[LandslideEvent]:
    statement = (
        select(LandslideEvent)
        .where(
            LandslideEvent.risk_zone_id == risk_zone_id
        )
        .order_by(
            LandslideEvent.occurred_at.desc()
        )
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )


def calculate_database_historical_risk_score(
    db: Session,
    *,
    risk_zone_id: int,
) -> float:
    event_count = get_historical_event_count(
        db=db,
        risk_zone_id=risk_zone_id,
        years=10,
    )

    if event_count >= 10:
        return 1.0

    if event_count >= 7:
        return 0.85

    if event_count >= 4:
        return 0.65

    if event_count >= 2:
        return 0.40

    if event_count == 1:
        return 0.20

    return 0.0


def calculate_gsi_spatial_risk_score(
    *,
    latitude: float,
    longitude: float,
) -> float:
    evidence = get_india_spatial_evidence(
        latitude,
        longitude,
    )

    within_1km = evidence["gsi_inventory_within_1km"]
    within_5km = evidence["gsi_inventory_within_5km"]
    within_10km = evidence["gsi_inventory_within_10km"]

    if within_1km >= 5:
        return 1.0

    if within_1km >= 2:
        return 0.90

    if within_1km >= 1:
        return 0.80

    if within_5km >= 10:
        return 0.75

    if within_5km >= 5:
        return 0.65

    if within_5km >= 1:
        return 0.50

    if within_10km >= 10:
        return 0.40

    if within_10km >= 5:
        return 0.30

    if within_10km >= 1:
        return 0.20

    return 0.0


def calculate_historical_risk_score(
    db: Session,
    *,
    risk_zone_id: int,
    latitude: float | None = None,
    longitude: float | None = None,
) -> float:
    database_score = calculate_database_historical_risk_score(
        db=db,
        risk_zone_id=risk_zone_id,
    )

    if latitude is None or longitude is None:
        return database_score

    gsi_score = calculate_gsi_spatial_risk_score(
        latitude=latitude,
        longitude=longitude,
    )

    # Keep both evidence sources without treating GSI proximity
    # as a calibrated landslide probability.
    return round(
        max(database_score, gsi_score),
        3,
    )
