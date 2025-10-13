"""Convert all IDs to UUID

Revision ID: e7ecfc4e0aed
Revises: d957030b6412
Create Date: [timestamp]

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e7ecfc4e0aed"
down_revision: Union[str, None] = "d957030b6412"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Convert all IDs to UUID and handle schema changes"""

    # Step 1: Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Step 2: Drop ALL foreign key constraints (including the one that's causing issues)
    constraints = [
        ("users", "users_organization_id_fkey"),
        ("users", "users_assigned_staff_id_fkey"),  # Added this one!
        ("users", "fk_user_assigned_staff_id"),
        ("org_members", "org_members_user_id_fkey"),
        ("org_members", "org_members_organization_id_fkey"),
        ("user_dashboards", "user_dashboards_user_id_fkey"),
    ]

    for table, constraint in constraints:
        try:
            op.execute(f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {constraint}")
        except Exception as e:
            print(f"Could not drop constraint {constraint}: {e}")
            pass

    # Step 2.5: Drop any other constraints we might have missed
    # Get all foreign key constraints and drop them
    connection = op.get_bind()
    try:
        # Query to find all foreign key constraints
        result = connection.execute(
            sa.text(
                """
            SELECT conname, conrelid::regclass 
            FROM pg_constraint 
            WHERE contype = 'f' 
            AND connamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
        """
            )
        )

        for constraint_name, table_name in result:
            try:
                op.execute(
                    f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint_name}"
                )
            except Exception:
                pass
    except Exception:
        pass

    # Step 3: Clear existing data (since we can't meaningfully convert integer IDs to UUIDs)
    op.execute("DELETE FROM user_dashboards")
    op.execute("DELETE FROM org_members")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM admin")

    # Step 4: Add/Remove columns first (before type conversion)
    # Add new columns
    op.add_column(
        "admin",
        sa.Column(
            "user_type",
            sa.Enum("USER", "ORGANIZATION", "ORG_MEMBER", "ADMIN", name="usertype"),
            nullable=True,
        ),
    )
    op.add_column(
        "organizations",
        sa.Column(
            "user_type",
            sa.Enum("USER", "ORGANIZATION", "ORG_MEMBER", "ADMIN", name="usertype"),
            nullable=True,
        ),
    )
    op.add_column(
        "organizations",
        sa.Column(
            "role", sa.Enum("ORG_ADMIN", "ORG_MEMBER", name="orgrole"), nullable=True
        ),
    )

    # Remove old columns
    op.drop_column("admin", "role")

    # Step 5: Convert ID columns to UUID
    tables = ["admin", "organizations", "users", "org_members", "user_dashboards"]

    for table in tables:
        # Drop sequence/default first
        op.execute(f"ALTER TABLE {table} ALTER COLUMN id DROP DEFAULT")
        # Convert to UUID
        op.execute(
            f"ALTER TABLE {table} ALTER COLUMN id TYPE UUID USING uuid_generate_v4()"
        )

    # Step 6: Convert foreign key columns
    fk_columns = [
        ("users", "organization_id"),
        ("users", "assigned_staff_id"),
        ("org_members", "user_id"),
        ("org_members", "organization_id"),
        ("user_dashboards", "user_id"),
    ]

    for table, column in fk_columns:
        op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE UUID USING NULL")

    # Step 7: Set default values for new enum columns
    op.execute("UPDATE admin SET user_type = 'ADMIN' WHERE user_type IS NULL")
    op.execute(
        "UPDATE organizations SET user_type = 'ORGANIZATION' WHERE user_type IS NULL"
    )
    op.execute("UPDATE organizations SET role = 'ORG_ADMIN' WHERE role IS NULL")

    # Step 8: Make enum columns NOT NULL
    op.alter_column("admin", "user_type", nullable=False)
    op.alter_column("organizations", "user_type", nullable=False)
    op.alter_column("organizations", "role", nullable=False)

    # Step 9: Recreate foreign key constraints
    op.create_foreign_key(
        "users_organization_id_fkey",
        "users",
        "organizations",
        ["organization_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "org_members_user_id_fkey",
        "org_members",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "org_members_organization_id_fkey",
        "org_members",
        "organizations",
        ["organization_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_user_assigned_staff_id",
        "users",
        "org_members",
        ["assigned_staff_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "user_dashboards_user_id_fkey",
        "user_dashboards",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Revert back to INTEGER IDs and old schema"""

    # Drop ALL foreign key constraints
    connection = op.get_bind()
    try:
        result = connection.execute(
            sa.text(
                """
            SELECT conname, conrelid::regclass 
            FROM pg_constraint 
            WHERE contype = 'f' 
            AND connamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
        """
            )
        )

        for constraint_name, table_name in result:
            try:
                op.execute(
                    f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint_name}"
                )
            except Exception:
                pass
    except Exception:
        pass

    # Clear data
    op.execute("DELETE FROM user_dashboards")
    op.execute("DELETE FROM org_members")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM admin")

    # Revert schema changes
    op.add_column("admin", sa.Column("role", sa.VARCHAR(), nullable=True))
    op.drop_column("admin", "user_type")
    op.drop_column("organizations", "user_type")
    op.drop_column("organizations", "role")

    # Convert foreign key columns back to INTEGER
    fk_columns = [
        ("users", "organization_id"),
        ("users", "assigned_staff_id"),
        ("org_members", "user_id"),
        ("org_members", "organization_id"),
        ("user_dashboards", "user_id"),
    ]

    for table, column in fk_columns:
        op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE INTEGER USING NULL")

    # Convert primary keys back to INTEGER with sequences
    tables = [
        ("admin", "admin_id_seq"),
        ("organizations", "organizations_id_seq"),
        ("users", "users_id_seq"),
        ("org_members", "org_members_id_seq"),
        ("user_dashboards", "user_dashboards_id_seq"),
    ]

    for table, seq in tables:
        op.execute(f"CREATE SEQUENCE IF NOT EXISTS {seq}")
        op.execute(f"ALTER TABLE {table} ALTER COLUMN id TYPE INTEGER USING 1")
        op.execute(f"ALTER TABLE {table} ALTER COLUMN id SET DEFAULT nextval('{seq}')")

    # Recreate original foreign key constraints
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
    op.create_foreign_key(
        "fk_user_assigned_staff_id",
        "users",
        "org_members",
        ["assigned_staff_id"],
        ["id"],
    )
    op.create_foreign_key(
        "user_dashboards_user_id_fkey", "user_dashboards", "users", ["user_id"], ["id"]
    )
