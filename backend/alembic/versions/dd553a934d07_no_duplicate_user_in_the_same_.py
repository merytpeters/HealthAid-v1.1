"""No duplicate user in the same organization

Revision ID: dd553a934d07
Revises: 767f2256735b
Create Date: 2025-10-13 22:05:21.281517

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dd553a934d07"
down_revision: Union[str, None] = "767f2256735b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
