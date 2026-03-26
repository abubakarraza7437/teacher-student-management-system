"""Add new teacher profile model

Revision ID: da3e16168654
Revises: 26e9a3412f6c
Create Date: 2026-03-26 17:18:10.991412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'da3e16168654'
down_revision: Union[str, Sequence[str], None] = '26e9a3412f6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'teacher_profile',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),    # noqa
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),  # noqa
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('left_at', sa.DateTime(), nullable=True),
        sa.Column('salary', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('teacher_profile')
