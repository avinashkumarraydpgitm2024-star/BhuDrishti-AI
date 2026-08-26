from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.models.road_segment import RoadSegment
from backend.app.schemas.road_segment import RoadSegmentCreate


def get_road_segment_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> RoadSegment | None:
    statement = select(RoadSegment).where(
        RoadSegment.public_id == public_id
    )
    return db.scalar(statement)


def get_road_segment_by_code(
    db: Session,
    *,
    road_code: str,
) -> RoadSegment | None:
    statement = select(RoadSegment).where(
        RoadSegment.road_code == road_code.upper()
    )
    return db.scalar(statement)


def get_risk_zone_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> RiskZone | None:
    statement = select(RiskZone).where(
        RiskZone.public_id == public_id
    )
    return db.scalar(statement)


def create_road_segment(
    db: Session,
    *,
    payload: RoadSegmentCreate,
) -> RoadSegment:
    risk_zone_id = None

    if payload.risk_zone_public_id is not None:
        risk_zone = get_risk_zone_by_public_id(
            db=db,
            public_id=payload.risk_zone_public_id,
        )

        if risk_zone is None:
            raise ValueError("Risk zone not found.")

        risk_zone_id = risk_zone.id

    road_segment = RoadSegment(
        road_code=payload.road_code.upper(),
        name=payload.name,
        road_type=payload.road_type,
        state=payload.state,
        district=payload.district,
        start_latitude=payload.start_latitude,
        start_longitude=payload.start_longitude,
        end_latitude=payload.end_latitude,
        end_longitude=payload.end_longitude,
        length_km=payload.length_km,
        risk_zone_id=risk_zone_id,
        is_blocked=payload.is_blocked,
        blockage_reason=payload.blockage_reason,
    )

    db.add(road_segment)
    db.commit()
    db.refresh(road_segment)

    return road_segment


def list_road_segments(
    db: Session,
    *,
    risk_zone_id: int | None = None,
    active_only: bool = True,
    blocked_only: bool = False,
) -> list[RoadSegment]:
    statement = select(RoadSegment)

    if risk_zone_id is not None:
        statement = statement.where(
            RoadSegment.risk_zone_id == risk_zone_id
        )

    if active_only:
        statement = statement.where(
            RoadSegment.is_active.is_(True)
        )

    if blocked_only:
        statement = statement.where(
            RoadSegment.is_blocked.is_(True)
        )

    statement = statement.order_by(
        RoadSegment.name.asc()
    )

    return list(db.scalars(statement).all())
