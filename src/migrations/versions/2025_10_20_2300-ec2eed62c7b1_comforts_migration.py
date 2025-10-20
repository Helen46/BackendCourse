"""comforts migration

Revision ID: ec2eed62c7b1
Revises: bb6a90557b6a
Create Date: 2025-10-20 23:00:35.621029

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ec2eed62c7b1"
down_revision: Union[str, None] = "bb6a90557b6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comforts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_comforts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("comfort_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["comfort_id"],
            ["comforts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms_comforts")
    op.drop_table("comforts")
