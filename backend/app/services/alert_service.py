from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.alert import Alert, AlertStatus
from backend.app.models.risk_assessment import RiskAssessment, RiskSeverity
from backend.app.models.risk_zone import RiskZone
from backend.app.schemas.alert import AlertCreate


def get_alert_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> Alert | None:
    return db.scalar(
        select(Alert).where(
            Alert.public_id == public_id
        )
    )


def get_risk_zone_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> RiskZone | None:
    return db.scalar(
        select(RiskZone).where(
            RiskZone.public_id == public_id
        )
    )


def get_risk_assessment_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> RiskAssessment | None:
    return db.scalar(
        select(RiskAssessment).where(
            RiskAssessment.public_id == public_id
        )
    )


def create_alert(
    db: Session,
    *,
    payload: AlertCreate,
) -> Alert:
    risk_zone = get_risk_zone_by_public_id(
        db=db,
        public_id=payload.risk_zone_public_id,
    )

    if risk_zone is None:
        raise ValueError("Risk zone not found.")

    risk_assessment_id = None

    if payload.risk_assessment_public_id is not None:
        assessment = get_risk_assessment_by_public_id(
            db=db,
            public_id=payload.risk_assessment_public_id,
        )

        if assessment is None:
            raise ValueError("Risk assessment not found.")

        if assessment.risk_zone_id != risk_zone.id:
            raise ValueError(
                "Risk assessment does not belong to the selected risk zone."
            )

        risk_assessment_id = assessment.id

    alert = Alert(
        risk_zone_id=risk_zone.id,
        risk_assessment_id=risk_assessment_id,
        severity=payload.severity,
        title=payload.title,
        message=payload.message,
        audience=payload.audience,
        status=AlertStatus.ACTIVE,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def list_alerts(
    db: Session,
    *,
    risk_zone_id: int | None = None,
    active_only: bool = False,
    limit: int = 100,
) -> list[Alert]:
    statement = select(Alert)

    if risk_zone_id is not None:
        statement = statement.where(
            Alert.risk_zone_id == risk_zone_id
        )

    if active_only:
        statement = statement.where(
            Alert.status == AlertStatus.ACTIVE
        )

    statement = (
        statement
        .order_by(Alert.created_at.desc())
        .limit(limit)
    )

    return list(db.scalars(statement).all())

def create_alert_from_assessment(
    db: Session,
    *,
    risk_zone: RiskZone,
    assessment: RiskAssessment,
) -> Alert | None:
    alertable_severities = {
        RiskSeverity.HIGH,
        RiskSeverity.VERY_HIGH,
        RiskSeverity.CRITICAL,
    }

    if assessment.severity not in alertable_severities:
        return None

    existing = db.scalar(
        select(Alert).where(
            Alert.risk_assessment_id == assessment.id,
            Alert.status == AlertStatus.ACTIVE,
        )
    )

    if existing is not None:
        return existing

    severity_label = assessment.severity.value.replace(
        "_",
        " ",
    ).title()

    alert = Alert(
        risk_zone_id=risk_zone.id,
        risk_assessment_id=assessment.id,
        severity=assessment.severity,
        title=f"{severity_label} Geo-Hazard Warning",
        message=(
            f"{risk_zone.name} has a "
            f"{assessment.risk_probability_percent:.1f}% "
            f"predicted landslide risk with "
            f"{severity_label.lower()} severity. "
            f"Dominant factor: "
            f"{assessment.dominant_factor or 'unknown'}."
        ),
        audience="authority",
        status=AlertStatus.ACTIVE,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def acknowledge_alert(
    db: Session,
    *,
    alert: Alert,
) -> Alert:
    from datetime import datetime, timezone

    if alert.status == AlertStatus.RESOLVED:
        raise ValueError(
            "Resolved alert cannot be acknowledged."
        )

    if alert.status == AlertStatus.ACKNOWLEDGED:
        return alert

    alert.status = AlertStatus.ACKNOWLEDGED
    alert.acknowledged_at = datetime.now(timezone.utc)

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def resolve_alert(
    db: Session,
    *,
    alert: Alert,
) -> Alert:
    from datetime import datetime, timezone

    if alert.status == AlertStatus.RESOLVED:
        return alert

    if alert.status == AlertStatus.ACTIVE:
        alert.acknowledged_at = (
            alert.acknowledged_at
            or datetime.now(timezone.utc)
        )

    alert.status = AlertStatus.RESOLVED
    alert.resolved_at = datetime.now(timezone.utc)

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert
