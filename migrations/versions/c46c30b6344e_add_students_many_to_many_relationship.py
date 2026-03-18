"""add students many-to-many relationship

Revision ID: c46c30b6344e
Revises: 2acfebda7050
Create Date: 2026-03-18 13:03:32.912813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c46c30b6344e'
down_revision: Union[str, Sequence[str], None] = '2acfebda7050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('class', 'students')
    op.create_table(
        'class_students',
        sa.Column('class_id', sa.Uuid(), nullable=False),
        sa.Column('student_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['class.id']),
        sa.ForeignKeyConstraint(['student_id'], ['user.id']),
        sa.PrimaryKeyConstraint('class_id', 'student_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('class_students')
    op.add_column(
        'class',
        sa.Column('students', sa.VARCHAR(), nullable=True),
    )
