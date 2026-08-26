from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.models.village import Village
from backend.app.schemas.village import VillageCreate


def get_village_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> Village | None:
    statement = select(Village).where(
        Village.public_id == public_id
    )
    return db.scalar(statement)


def get_village_by_code(
    db: Session,
    *,
    village_code: str,
) -> Village | None:
    statement = select(Village).where(
        Village.village_code == village_code.upper()
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


def create_village(
    db: Session,
    *,
    payload: VillageCreate,
) -> Village:
    risk_zone_id = None

    if payload.risk_zone_public_id is not None:
        risk_zone = get_risk_zone_by_public_id(
            db=db,
            public_id=payload.risk_zone_public_id,
        )

        if risk_zone is None:
            raise ValueError("Risk zone not found.")

        risk_zone_id = risk_zone.id

    village = Village(
        village_code=payload.village_code.upper(),
        name=payload.name,
        state=payload.state,
        district=payload.district,
        latitude=payload.latitude,
        longitude=payload.longitude,
        elevation_m=payload.elevation_m,
        population=payload.population,
        risk_zone_id=risk_zone_id,
        has_health_facility=payload.has_health_facility,
        has_school=payload.has_school,
        is_accessible=payload.is_accessible,
    )

    db.add(village)
    db.commit()
    db.refresh(village)

    return village


def list_villages(
    db: Session,
    *,
    risk_zone_id: int | None = None,
    active_only: bool = True,
) -> list[Village]:
    statement = select(Village)

    if risk_zone_id is not None:
        statement = statement.where(
            Village.risk_zone_id == risk_zone_id
        )

    if active_only:
        statement = statement.where(
            Village.is_active.is_(True)
        )

    statement = statement.order_by(Village.name.asc())

    return list(db.scalars(statement).all())
