"""do email unique

Revision ID: 53f03c33a5fb
Revises: 468151def8d0
Create Date: 2024-09-16 00:12:37.020498

"""

from typing import Sequence, Union

from alembic import op


revision: str = "53f03c33a5fb"
down_revision: Union[str, None] = "468151def8d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
