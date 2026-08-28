from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertDeliveryCreate(BaseModel):
    alert_public_id: str = Field(
        min_length=36,
        max_length=36,
    )

    channel: str = Field(
        min_length=2,
        max_length=30,
    )

    recipient: str = Field(
        min_length=2,
        max_length=255,
    )

    provider: str | None = Field(
        default=None,
        max_length=100,
    )


class AlertDeliveryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: str
    alert_id: int
    channel: str
    recipient: str
    status: str

    provider: str | None
    provider_message_id: str | None
    error_message: str | None

    retry_count: int

    created_at: datetime
    sent_at: datetime | None
    delivered_at: datetime | None
