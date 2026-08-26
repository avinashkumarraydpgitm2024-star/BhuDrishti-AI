from sqlalchemy.orm import Session

from backend.app.models.risk_zone import RiskZone
from backend.app.services.risk_assessment_service import (
    get_latest_risk_assessment,
)
from backend.app.services.road_segment_service import (
    list_road_segments,
)
from backend.app.services.village_service import (
    list_villages,
)


def build_gis_map_data(
    db: Session,
    *,
    risk_zone: RiskZone,
) -> dict:
    villages = list_villages(
        db=db,
        risk_zone_id=risk_zone.id,
    )

    road_segments = list_road_segments(
        db=db,
        risk_zone_id=risk_zone.id,
    )

    latest_assessment = get_latest_risk_assessment(
        db=db,
        risk_zone_id=risk_zone.id,
    )

    blocked_road_count = sum(
        road.is_blocked
        for road in road_segments
    )

    return {
        "risk_zone": risk_zone,
        "latest_risk_assessment": latest_assessment,
        "villages": villages,
        "road_segments": road_segments,
        "village_count": len(villages),
        "road_segment_count": len(road_segments),
        "blocked_road_count": blocked_road_count,
    }
