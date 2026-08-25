"""Add data quality status to sensor readings

Revision ID: cc53557f7fd8
Revises: 45df57b42be9
Create Date: 2026-08-23 23:43:02.451615
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "cc53557f7fd8"
down_revision: Union[str, Sequence[str], None] = "45df57b42be9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_index(
        op.f("ix_sensor_readings_data_quality_status"),
        "sensor_readings",
        ["data_quality_status"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_sensor_readings_data_quality_status"),
        table_name="sensor_readings",
    )

    op.drop_column(
        "sensor_readings",
        "data_quality_status",
    )