from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.landslide_event import LandslideEvent
from backend.app.models.risk_zone import RiskZone
from backend.app.schemas.landslide_event import LandslideEventCreate


def get_risk_zone_by_public_id(
    db: Session,
    public_id: str,
) -> RiskZone | None:
    statement = select(RiskZone).where(
        RiskZone.public_id == public_id
    )

    return db.scalar(statement)


def get_landslide_event_by_code(
    db: Session,
    event_code: str,
) -> LandslideEvent | None:
    statement = select(LandslideEvent).where(
        LandslideEvent.event_code == event_code.strip().upper()
    )

    return db.scalar(statement)


def get_landslide_event_by_public_id(
    db: Session,
    public_id: str,
) -> LandslideEvent | None:
    statement = select(LandslideEvent).where(
        LandslideEvent.public_id == public_id
    )

    return db.scalar(statement)


def create_landslide_event(
    db: Session,
    event_data: LandslideEventCreate,
) -> LandslideEvent:
    event_code = event_data.event_code.strip().upper()

    existing = get_landslide_event_by_code(
        db=db,
        event_code=event_code,
    )

    if existing is not None:
        raise ValueError(
            "Landslide event code already exists."
        )

    risk_zone_id = None

    if event_data.risk_zone_public_id is not None:
        risk_zone = get_risk_zone_by_public_id(
            db=db,
            public_id=event_data.risk_zone_public_id,
        )

        if risk_zone is None:
            raise ValueError(
                "Risk zone not found."
            )

        risk_zone_id = risk_zone.id

    event = LandslideEvent(
        risk_zone_id=risk_zone_id,
        event_code=event_code,
        state=event_data.state.strip(),
        district=event_data.district.strip(),
        latitude=event_data.latitude,
        longitude=event_data.longitude,
        occurred_at=event_data.occurred_at,
        severity=event_data.severity,
        rainfall_24h_mm=event_data.rainfall_24h_mm,
        soil_moisture_percent=(
            event_data.soil_moisture_percent
        ),
        slope_degrees=event_data.slope_degrees,
        fatalities=event_data.fatalities,
        injuries=event_data.injuries,
        affected_area_sq_km=(
            event_data.affected_area_sq_km
        ),
        road_blocked=event_data.road_blocked,
        source=(
            event_data.source.strip()
            if event_data.source
            else None
        ),
        description=(
            event_data.description.strip()
            if event_data.description
            else None
        ),
    )

    db.add(event)

    try:
        db.commit()
        db.refresh(event)

    except Exception:
        db.rollback()
        raise

    return event


def list_landslide_events(
    db: Session,
    *,
    state: str | None = None,
    district: str | None = None,
    risk_zone_id: int | None = None,
    limit: int = 100,
) -> list[LandslideEvent]:
    statement = select(LandslideEvent)

    if state is not None:
        statement = statement.where(
            LandslideEvent.state == state.strip()
        )

    if district is not None:
        statement = statement.where(
            LandslideEvent.district == district.strip()
        )

    if risk_zone_id is not None:
        statement = statement.where(
            LandslideEvent.risk_zone_id == risk_zone_id
        )

    statement = (
        statement
        .order_by(
            LandslideEvent.occurred_at.desc()
        )
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )
