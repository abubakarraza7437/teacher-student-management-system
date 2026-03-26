"""adjust table issues

Revision ID: 877082ccd3bb
Revises: b3989f1dabf2
Create Date: 2026-03-26 16:34:01.190263

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '877082ccd3bb'
down_revision: Union[str, Sequence[str], None] = 'b3989f1dabf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
