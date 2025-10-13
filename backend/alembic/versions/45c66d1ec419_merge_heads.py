"""merge heads

Revision ID: 45c66d1ec419
Revises: dd553a934d07
Create Date: 2025-10-13 22:18:01.731486

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45c66d1ec419"
down_revision: Union[str, None] = "dd553a934d07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
