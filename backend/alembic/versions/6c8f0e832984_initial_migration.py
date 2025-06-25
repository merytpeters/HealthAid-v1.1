"""Initial migration

Revision ID: 6c8f0e832984
Revises: 82d26691e6a3
Create Date: 2025-06-22 14:24:16.409565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c8f0e832984'
down_revision: Union[str, None] = '82d26691e6a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
