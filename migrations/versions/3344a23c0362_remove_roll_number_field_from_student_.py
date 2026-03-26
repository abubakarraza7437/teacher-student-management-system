"""remove roll number field from student profile

Revision ID: 3344a23c0362
Revises: da3e16168654
Create Date: 2026-03-26 17:46:24.504937

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '3344a23c0362'
down_revision: Union[str, Sequence[str], None] = 'da3e16168654'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
