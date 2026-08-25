from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.schemas.risk_zone import RiskZoneCreate


def get_risk_zone_by_code(
    db: Session,
    zone_code: str,
) -> RiskZone | None:
    normalized_code = zone_code.strip().upper()

    statement = select(RiskZone).where(
        RiskZone.zone_code == normalized_code
    )

    return db.scalar(statement)


def get_risk_zone_by_public_id(
    db: Session,
    public_id: str,
) -> RiskZone | None:
    statement = select(RiskZone).where(
        RiskZone.public_id == public_id
    )

    return db.scalar(statement)


def create_risk_zone(
    db: Session,
    zone_data: RiskZoneCreate,
) -> RiskZone:
    zone = RiskZone(
        zone_code=zone_data.zone_code.strip().upper(),
        name=zone_data.name.strip(),
        state=zone_data.state.strip(),
        district=zone_data.district.strip(),
        latitude=zone_data.latitude,
        longitude=zone_data.longitude,
        elevation_m=zone_data.elevation_m,
        slope_degrees=zone_data.slope_degrees,
        area_sq_km=zone_data.area_sq_km,
        terrain_type=(
            zone_data.terrain_type.strip()
            if zone_data.terrain_type
            else None
        ),
        description=(
            zone_data.description.strip()
            if zone_data.description
            else None
        ),
        grid_resolution_m=zone_data.grid_resolution_m,
    )

    db.add(zone)

    try:
        db.commit()
        db.refresh(zone)
    except Exception:
        db.rollback()
        raise

    return zone


def list_risk_zones(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[RiskZone]:
    statement = (
        select(RiskZone)
        .where(RiskZone.is_active.is_(True))
        .order_by(RiskZone.state, RiskZone.district, RiskZone.zone_code)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())