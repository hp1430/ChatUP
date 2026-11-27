"""index chatup_threads user_id

Revision ID: 352bb8350f5e
Revises: 4696b8bddc01
Create Date: 2026-11-27 20:48:28.922413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '352bb8350f5e'
down_revision: Union[str, Sequence[str], None] = '4696b8bddc01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        'ix_chatup_threads_user_id',
        'chatup_threads',
        ['user_id'],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_chatup_threads_user_id', table_name='chatup_threads')
