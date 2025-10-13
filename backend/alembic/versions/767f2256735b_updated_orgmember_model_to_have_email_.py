"""Updated OrgMember Model to have email, name and username fields and made user_id field nullable so orgMember can be independent of user model

Revision ID: 767f2256735b
Revises: e7ecfc4e0aed
Create Date: 2025-10-13 20:18:52.694996

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "767f2256735b"
down_revision: Union[str, None] = "e7ecfc4e0aed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if columns exist before adding them
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col["name"] for col in inspector.get_columns("org_members")]

    # Add missing columns if they don't exist
    if "username" not in columns:
        op.add_column("org_members", sa.Column("username", sa.String(), nullable=True))
        op.create_index(
            op.f("ix_org_members_username"), "org_members", ["username"], unique=False
        )

    if "email" not in columns:
        op.add_column("org_members", sa.Column("email", sa.String(), nullable=True))
        op.create_index(
            op.f("ix_org_members_email"), "org_members", ["email"], unique=False
        )

    if "full_name" not in columns:
        op.add_column("org_members", sa.Column("full_name", sa.String(), nullable=True))

    if "hashed_password" not in columns:
        op.add_column(
            "org_members", sa.Column("hashed_password", sa.String(), nullable=True)
        )

    # Make user_id nullable if it isn't already
    op.alter_column("org_members", "user_id", nullable=True)

    # Add unique constraint for user_id + organization_id if it doesn't exist
    try:
        op.create_unique_constraint(
            "unique_user_per_org", "org_members", ["user_id", "organization_id"]
        )
    except Exception:
        # Constraint might already exist
        pass


def downgrade() -> None:
    # Remove the unique constraint
    try:
        op.drop_constraint("unique_user_per_org", "org_members", type_="unique")
    except Exception:
        pass

    # Make user_id not nullable
    op.alter_column("org_members", "user_id", nullable=False)

    # Remove added columns
    op.drop_column("org_members", "hashed_password")
    op.drop_column("org_members", "full_name")
    op.drop_index(op.f("ix_org_members_email"), table_name="org_members")
    op.drop_column("org_members", "email")
    op.drop_index(op.f("ix_org_members_username"), table_name="org_members")
    op.drop_column("org_members", "username")
