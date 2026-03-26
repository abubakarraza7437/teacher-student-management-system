"""Add new teacher profile model

Revision ID: 26e9a3412f6c
Revises: 877082ccd3bb
Create Date: 2026-03-26 17:13:47.861719

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '26e9a3412f6c'
down_revision: Union[str, Sequence[str], None] = '877082ccd3bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
