"""add rooms table

Revision ID: 4ab3d59aad3a
Revises: 21ea6fce2d97
Create Date: 2024-09-15 14:26:29.297160

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4ab3d59aad3a"
down_revision: Union[str, None] = "21ea6fce2d97"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
