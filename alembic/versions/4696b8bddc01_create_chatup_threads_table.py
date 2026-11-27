"""create chatup_threads table

Revision ID: 4696b8bddc01
Revises: 0b84c65ea90c
Create Date: 2026-11-27 20:55:57.342127

"""
from pickle import FALSE
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4696b8bddc01'
down_revision: Union[str, Sequence[str], None] = '0b84c65ea90c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "chatup_threads",
        sa.Column("thread_id", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("thread_id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["chatup_users.user_id"],
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("chatup_threads")
