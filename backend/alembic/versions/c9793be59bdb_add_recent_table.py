"""Add recent table

Revision ID: c9793be59bdb
Revises: b66789a50a7c
Create Date: 2025-06-25 14:12:16.885773

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "c9793be59bdb"
down_revision: Union[str, None] = "b66789a50a7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the Enum with create_type=False and native_enum=False to avoid auto-creating PostgreSQL enum type
role_enum = sa.Enum(
    "ADMIN",
    "USER",
    "ORGANIZATION",
    name="usertype",
    create_type=False,
    native_enum=False,
)


def upgrade() -> None:
    conn = op.get_bind()
    # Manually create enum type only if it doesn't exist
    conn.execute(
        text(
            """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'usertype') THEN
            CREATE TYPE usertype AS ENUM ('ADMIN', 'USER', 'ORGANIZATION');
        END IF;
    END$$;
    """
        )
    )

    # Create table using the Enum without recreating the enum type
    op.create_table(
        "admin",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("role", role_enum, nullable=False),
        sa.Column("is_admin", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admin_id"), "admin", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_admin_id"), table_name="admin")
    op.drop_table("admin")
