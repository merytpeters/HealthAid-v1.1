"""Fix multi-organization membership for org_members

Revision ID: fix_multi_org_membership
Revises: e4995b22ad2a
Create Date: 2024-01-01 00:00:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fix_multi_org_membership"
down_revision: Union[str, None] = "e4995b22ad2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check what exists in the database
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Check if table exists
    if not inspector.has_table("org_members"):
        print("org_members table does not exist, skipping...")
        return

    # Get current columns
    columns = {col["name"]: col for col in inspector.get_columns("org_members")}

    # Add new columns if they don't exist
    if "is_active" not in columns:
        op.add_column(
            "org_members",
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        )
        print("Added is_active column")
    else:
        print("is_active column already exists")

    if "joined_at" not in columns:
        op.add_column(
            "org_members",
            sa.Column(
                "joined_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
            ),
        )
        print("Added joined_at column")
    else:
        print("joined_at column already exists")

    # Drop unique constraint if it exists
    try:
        constraints = inspector.get_unique_constraints("org_members")
        for constraint in constraints:
            if constraint["name"] == "unique_user_per_org":
                op.drop_constraint("unique_user_per_org", "org_members", type_="unique")
                print("Dropped unique_user_per_org constraint")
                break
    except Exception as e:
        print(f"Constraint handling: {e}")


def downgrade() -> None:
    # This is optional - you can leave it empty for now
    pass
