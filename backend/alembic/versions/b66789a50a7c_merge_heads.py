"""merge heads

Revision ID: b66789a50a7c
Revises: 6c8f0e832984, 701d6cdf5731
Create Date: 2025-06-25 14:01:16.882912

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b66789a50a7c"
down_revision: Union[str, None] = ("6c8f0e832984", "701d6cdf5731")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
