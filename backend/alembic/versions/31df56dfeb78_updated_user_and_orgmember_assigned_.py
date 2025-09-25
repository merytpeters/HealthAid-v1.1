"""Updated user and orgmember assigned relationship

Revision ID: 31df56dfeb78
Revises: 18032ec4f0d4
Create Date: 2025-06-27 13:41:16.493767
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "31df56dfeb78"
down_revision: Union[str, None] = "18032ec4f0d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Convert admin.role to Enum
    op.alter_column(
        "admin",
        "role",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.Enum("ADMIN", "USER", "ORGANIZATION", name="usertype"),
        existing_nullable=False,
        postgresql_using="role::usertype",
    )

    # Step 2: Drop all foreign keys that rely on columns we want to change
    op.drop_constraint("org_members_user_id_fkey", "org_members", type_="foreignkey")
    op.drop_constraint(
        "org_members_organization_id_fkey", "org_members", type_="foreignkey"
    )
    op.drop_constraint("users_assigned_staff_id_fkey", "users", type_="foreignkey")
    op.drop_constraint("users_organization_id_fkey", "users", type_="foreignkey")

    # Step 3: Alter primary key types
    op.alter_column(
        "organizations",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
        existing_server_default="nextval('organizations_id_seq'::regclass)",
    )

    op.alter_column(
        "users",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
    )

    # Step 4: Alter foreign key columns
    op.alter_column(
        "users",
        "organization_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "users",
        "assigned_staff_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "org_members",
        "user_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "org_members",
        "organization_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
    )

    # Step 5: Re-create foreign key constraints
    op.create_foreign_key(
        "users_assigned_staff_id_fkey",
        "users",
        "org_members",
        ["assigned_staff_id"],
        ["id"],
    )
    op.create_foreign_key(
        "users_organization_id_fkey",
        "users",
        "organizations",
        ["organization_id"],
        ["id"],
    )
    op.create_foreign_key(
        "org_members_user_id_fkey", "org_members", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "org_members_organization_id_fkey",
        "org_members",
        "organizations",
        ["organization_id"],
        ["id"],
    )


def downgrade() -> None:
    # Drop updated foreign keys
    op.drop_constraint("org_members_user_id_fkey", "org_members", type_="foreignkey")
    op.drop_constraint("users_assigned_staff_id_fkey", "users", type_="foreignkey")

    # Revert foreign key columns in org_members
    op.alter_column(
        "org_members",
        "organization_id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )

    op.alter_column(
        "org_members",
        "user_id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )

    # Revert foreign key columns in users
    op.alter_column(
        "users",
        "assigned_staff_id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )

    op.alter_column(
        "users",
        "organization_id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )

    # Revert primary key in users and organizations
    op.alter_column(
        "users",
        "id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )

    op.alter_column(
        "organizations",
        "id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        existing_server_default="nextval('organizations_id_seq'::regclass)",
    )

    # Recreate old foreign keys
    op.create_foreign_key(
        "users_assigned_staff_id_fkey",
        "users",
        "org_members",
        ["assigned_staff_id"],
        ["id"],
    )
    op.create_foreign_key(
        "org_members_user_id_fkey", "org_members", "users", ["user_id"], ["id"]
    )

    # Revert admin.role to VARCHAR
    op.alter_column(
        "admin",
        "role",
        existing_type=sa.Enum("ADMIN", "USER", "ORGANIZATION", name="usertype"),
        type_=sa.VARCHAR(length=12),
        existing_nullable=False,
    )
