"""create init tables

Revision ID: f4216bc86215
Revises: 
Create Date: 2026-07-26 14:57:36.841175

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f4216bc86215'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # op.create_table("Posts", sa.Column("Id", sa.Integer(), nullable= False, primary_key=True), sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # op.drop_table("Posts")
    pass
