"""Enable multi-organization membership for org_members

Revision ID: enable_multi_org_membership
Revises: e4995b22ad2a
Create Date: 2024-01-01 00:00:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "enable_multi_org_membership"
down_revision: Union[str, None] = "e4995b22ad2a"  # Updated to current head
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if the unique constraint exists before trying to drop it
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    constraints = inspector.get_unique_constraints("org_members")

    # Drop the unique constraint if it exists
    for constraint in constraints:
        if constraint["name"] == "unique_user_per_org":
            op.drop_constraint("unique_user_per_org", "org_members", type_="unique")
            break

    # Check if columns exist before adding them
    columns = [col["name"] for col in inspector.get_columns("org_members")]

    # Add new fields for membership tracking if they don't exist
    if "is_active" not in columns:
        op.add_column(
            "org_members",
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        )

    if "joined_at" not in columns:
        op.add_column(
            "org_members",
            sa.Column(
                "joined_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
            ),
        )


def downgrade() -> None:
    # Remove the new columns
    op.drop_column("org_members", "joined_at")
    op.drop_column("org_members", "is_active")

    # Note: We don't recreate the unique constraint in downgrade because
    # there might be duplicate memberships that would cause the constraint to fail
    # If you need to recreate it, you'd need to clean up duplicates first
