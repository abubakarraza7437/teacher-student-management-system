"""remove roll number field from student profile

Revision ID: 89420ce2c67f
Revises: 3344a23c0362
Create Date: 2026-03-26 17:56:06.153692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '89420ce2c67f'
down_revision: Union[str, Sequence[str], None] = '3344a23c0362'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Use batch_alter_table for SQLite to drop columns by recreating the table.
    with op.batch_alter_table(
            'student_profile',
            recreate='always'
    ) as batch_op:
        batch_op.drop_column('classes')
        batch_op.drop_column('roll_number')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the previous structure by adding the columns back.
    with op.batch_alter_table(
            'student_profile',
            recreate='always'
    ) as batch_op:
        batch_op.add_column(sa.Column(
            'roll_number',
            sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column(
            'classes',
            sa.CHAR(length=32), nullable=False))
        batch_op.create_foreign_key(
            None,
            'class',
            ['classes'],
            ['id']
        )
