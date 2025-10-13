"""Add missing columns to org_members table

Revision ID: add_org_member_columns
Revises: [previous_revision_id]
Create Date: 2024-01-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "add_org_member_columns"
down_revision = None  # Replace with actual previous revision
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add missing columns to org_members table
    op.add_column("org_members", sa.Column("username", sa.String(), nullable=True))
    op.add_column("org_members", sa.Column("email", sa.String(), nullable=True))
    op.add_column("org_members", sa.Column("full_name", sa.String(), nullable=True))
    op.add_column(
        "org_members", sa.Column("hashed_password", sa.String(), nullable=True)
    )

    # Add indexes
    op.create_index(
        op.f("ix_org_members_username"), "org_members", ["username"], unique=False
    )
    op.create_index(
        op.f("ix_org_members_email"), "org_members", ["email"], unique=False
    )

    # Update existing records to have non-null values (if any exist)
    # You may need to customize this based on your existing data

    # After adding columns, make them NOT NULL
    op.alter_column("org_members", "username", nullable=False)
    op.alter_column("org_members", "email", nullable=False)
    op.alter_column("org_members", "full_name", nullable=False)
    op.alter_column("org_members", "hashed_password", nullable=False)


def downgrade() -> None:
    # Remove the added columns
    op.drop_index(op.f("ix_org_members_email"), table_name="org_members")
    op.drop_index(op.f("ix_org_members_username"), table_name="org_members")
    op.drop_column("org_members", "hashed_password")
    op.drop_column("org_members", "full_name")
    op.drop_column("org_members", "email")
    op.drop_column("org_members", "username")
