"""baseline existing schema

Revision ID: 43d653dfb19d
Revises: 
Create Date: 2026-09-26 21:51:20.123473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43d653dfb19d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "issues",
        sa.Column("id", sa.Integer(), sa.Identity(always=True), nullable=False),
        sa.Column("room", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("issues")
