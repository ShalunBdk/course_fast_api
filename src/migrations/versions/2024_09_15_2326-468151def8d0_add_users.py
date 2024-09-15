"""add users

Revision ID: 468151def8d0
Revises: 4ab3d59aad3a
Create Date: 2024-09-15 23:26:14.076583

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "468151def8d0"
down_revision: Union[str, None] = "4ab3d59aad3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
