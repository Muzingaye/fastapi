"""create init tables

Revision ID: 6ce37ec4f213
Revises: f4216bc86215
Create Date: 2026-07-26 15:51:13.408496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ce37ec4f213'
down_revision: Union[str, Sequence[str], None] = 'f4216bc86215'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
