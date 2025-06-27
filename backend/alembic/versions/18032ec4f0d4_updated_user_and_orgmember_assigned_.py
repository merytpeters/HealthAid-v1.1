"""Updated user and orgmember assigned relationship

Revision ID: 18032ec4f0d4
Revises: c9793be59bdb
Create Date: 2025-06-27 13:39:21.000264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18032ec4f0d4'
down_revision: Union[str, None] = 'c9793be59bdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
