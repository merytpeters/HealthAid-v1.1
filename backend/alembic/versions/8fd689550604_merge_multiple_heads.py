"""merge multiple heads

Revision ID: 8fd689550604
Revises: 45c66d1ec419, enable_multi_org_membership
Create Date: 2025-10-13 23:08:00.226331

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8fd689550604"
down_revision: Union[str, None] = ("45c66d1ec419", "enable_multi_org_membership")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
