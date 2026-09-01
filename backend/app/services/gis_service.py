from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.alert import Alert, AlertStatus
from backend.app.models.alert_delivery import (
    AlertDelivery,
    DeliveryStatus,
)
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
from backend.app.services.satellite_observation_service import (
    get_latest_satellite_observation_for_zone,
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

    latest_satellite_observation = (
        get_latest_satellite_observation_for_zone(
            db=db,
            risk_zone_id=risk_zone.id,
        )
    )

    active_alerts = list(
        db.scalars(
            select(Alert)
            .where(
                Alert.risk_zone_id == risk_zone.id,
                Alert.status == AlertStatus.ACTIVE,
            )
            .order_by(Alert.created_at.desc())
        ).all()
    )

    blocked_road_count = sum(
        road.is_blocked
        for road in road_segments
    )

    delivered_notification_count = db.scalar(
        select(func.count())
        .select_from(AlertDelivery)
        .join(
            Alert,
            AlertDelivery.alert_id == Alert.id,
        )
        .where(
            Alert.risk_zone_id == risk_zone.id,
            AlertDelivery.status == DeliveryStatus.DELIVERED,
        )
    ) or 0

    failed_notification_count = db.scalar(
        select(func.count())
        .select_from(AlertDelivery)
        .join(
            Alert,
            AlertDelivery.alert_id == Alert.id,
        )
        .where(
            Alert.risk_zone_id == risk_zone.id,
            AlertDelivery.status == DeliveryStatus.FAILED,
        )
    ) or 0

    return {
        "risk_zone": risk_zone,
        "latest_risk_assessment": latest_assessment,
        "latest_satellite_observation": latest_satellite_observation,
        "active_alerts": active_alerts,
        "villages": villages,
        "road_segments": road_segments,
        "village_count": len(villages),
        "road_segment_count": len(road_segments),
        "blocked_road_count": blocked_road_count,
        "active_alert_count": len(active_alerts),
        "delivered_notification_count": delivered_notification_count,
        "failed_notification_count": failed_notification_count,
    }

