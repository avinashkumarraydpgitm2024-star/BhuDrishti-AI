"""add Assam landslide dataset

Revision ID: 0ee18600d94c
Revises: 9531735357bb
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0ee18600d94c"
down_revision: Union[str, Sequence[str], None] = "9531735357bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assam_landslide_dataset",

        sa.Column("record_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("district", sa.String(100), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("elevation_m", sa.Float(), nullable=False),
        sa.Column("slope_deg", sa.Float(), nullable=False),
        sa.Column("rainfall_24h_mm", sa.Float(), nullable=False),
        sa.Column("rainfall_72h_mm", sa.Float(), nullable=False),
        sa.Column("rainfall_7d_mm", sa.Float(), nullable=False),
        sa.Column("soil_moisture_index", sa.Float(), nullable=False),
        sa.Column("soil_type", sa.String(100), nullable=False),
        sa.Column("geology", sa.String(100), nullable=False),
        sa.Column("land_cover", sa.String(100), nullable=False),
        sa.Column("ndvi", sa.Float(), nullable=False),
        sa.Column("road_distance_km", sa.Float(), nullable=False),
        sa.Column("river_distance_km", sa.Float(), nullable=False),
        sa.Column("road_cutting", sa.Integer(), nullable=False),
        sa.Column("deforestation_index", sa.Float(), nullable=False),
        sa.Column("landslide_occurrence", sa.Integer(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(30), nullable=False),
    )

    op.create_index(
        "ix_assam_landslide_dataset_district",
        "assam_landslide_dataset",
        ["district"],
    )

    op.create_index(
        "ix_assam_landslide_dataset_coordinates",
        "assam_landslide_dataset",
        ["latitude", "longitude"],
    )

    op.create_index(
        "ix_assam_landslide_dataset_occurrence",
        "assam_landslide_dataset",
        ["landslide_occurrence"],
    )

    op.create_index(
        "ix_assam_landslide_dataset_risk_level",
        "assam_landslide_dataset",
        ["risk_level"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_assam_landslide_dataset_risk_level",
        table_name="assam_landslide_dataset",
    )

    op.drop_index(
        "ix_assam_landslide_dataset_occurrence",
        table_name="assam_landslide_dataset",
    )

    op.drop_index(
        "ix_assam_landslide_dataset_coordinates",
        table_name="assam_landslide_dataset",
    )

    op.drop_index(
        "ix_assam_landslide_dataset_district",
        table_name="assam_landslide_dataset",
    )

    op.drop_table("assam_landslide_dataset")
