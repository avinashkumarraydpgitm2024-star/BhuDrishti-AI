from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.alert import Alert
from backend.app.models.alert_delivery import (
    AlertDelivery,
    DeliveryStatus,
    NotificationChannel,
)
from backend.app.schemas.alert_delivery import AlertDeliveryCreate


VALID_CHANNELS = {
    NotificationChannel.EMAIL,
    NotificationChannel.SMS,
    NotificationChannel.PUSH,
    NotificationChannel.IN_APP,
}


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


def get_delivery_by_public_id(
    db: Session,
    *,
    public_id: str,
) -> AlertDelivery | None:
    return db.scalar(
        select(AlertDelivery).where(
            AlertDelivery.public_id == public_id
        )
    )


def create_alert_delivery(
    db: Session,
    *,
    payload: AlertDeliveryCreate,
) -> AlertDelivery:
    alert = get_alert_by_public_id(
        db=db,
        public_id=payload.alert_public_id,
    )

    if alert is None:
        raise ValueError("Alert not found.")

    channel = payload.channel.lower().strip()

    if channel not in VALID_CHANNELS:
        raise ValueError(
            "Unsupported notification channel."
        )

    delivery = AlertDelivery(
        alert_id=alert.id,
        channel=channel,
        recipient=payload.recipient,
        provider=payload.provider,
        status=DeliveryStatus.PENDING,
    )

    db.add(delivery)
    db.commit()
    db.refresh(delivery)

    return delivery


def mark_delivery_sent(
    db: Session,
    *,
    delivery: AlertDelivery,
    provider_message_id: str | None = None,
) -> AlertDelivery:
    delivery.status = DeliveryStatus.SENT
    delivery.provider_message_id = provider_message_id
    delivery.sent_at = datetime.now(timezone.utc)
    delivery.error_message = None

    db.add(delivery)
    db.commit()
    db.refresh(delivery)

    return delivery


def mark_delivery_delivered(
    db: Session,
    *,
    delivery: AlertDelivery,
) -> AlertDelivery:
    delivery.status = DeliveryStatus.DELIVERED
    delivery.delivered_at = datetime.now(timezone.utc)

    if delivery.sent_at is None:
        delivery.sent_at = delivery.delivered_at

    db.add(delivery)
    db.commit()
    db.refresh(delivery)

    return delivery


def mark_delivery_failed(
    db: Session,
    *,
    delivery: AlertDelivery,
    error_message: str,
) -> AlertDelivery:
    delivery.status = DeliveryStatus.FAILED
    delivery.error_message = error_message
    delivery.retry_count += 1

    db.add(delivery)
    db.commit()
    db.refresh(delivery)

    return delivery


def list_alert_deliveries(
    db: Session,
    *,
    alert_id: int | None = None,
    limit: int = 100,
) -> list[AlertDelivery]:
    statement = select(AlertDelivery)

    if alert_id is not None:
        statement = statement.where(
            AlertDelivery.alert_id == alert_id
        )

    statement = (
        statement
        .order_by(AlertDelivery.created_at.desc())
        .limit(limit)
    )

    return list(db.scalars(statement).all())
