"""Add unique constraint to weather forecasts

Revision ID: 9e9b704c7a8a
Revises: 5fdec5f4e52d
Create Date: 2026-08-25 21:01:11.815045

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9e9b704c7a8a"
down_revision: Union[str, Sequence[str], None] = "5fdec5f4e52d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("weather_forecasts") as batch_op:
        batch_op.create_unique_constraint(
            "uq_weather_forecast_location_time",
            [
                "provider",
                "latitude",
                "longitude",
                "forecast_for",
            ],
        )


def downgrade() -> None:
    with op.batch_alter_table("weather_forecasts") as batch_op:
        batch_op.drop_constraint(
            "uq_weather_forecast_location_time",
            type_="unique",
        )