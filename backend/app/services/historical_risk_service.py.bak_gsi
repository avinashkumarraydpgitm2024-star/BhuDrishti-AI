from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.landslide_event import LandslideEvent


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


def calculate_historical_risk_score(
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