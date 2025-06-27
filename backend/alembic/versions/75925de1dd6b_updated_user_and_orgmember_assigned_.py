"""Updated user and orgmember assigned relationship

Revision ID: 75925de1dd6b
Revises: 31df56dfeb78
Create Date: 2025-06-27 14:03:03.439496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75925de1dd6b'
down_revision: Union[str, None] = '31df56dfeb78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ Drop ALL foreign key constraints that reference anything being altered
    op.drop_constraint('users_assigned_staff_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_organization_id_fkey', 'users', type_='foreignkey')  # ✅ ADD THIS
    op.drop_constraint('org_members_user_id_fkey', 'org_members', type_='foreignkey')
    op.drop_constraint('org_members_organization_id_fkey', 'org_members', type_='foreignkey')

    # Step 1: Alter referenced table columns FIRST
    op.execute("ALTER TABLE organizations ALTER COLUMN id TYPE INTEGER USING id::integer")
    op.alter_column('organizations', 'id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default="nextval('organizations_id_seq'::regclass)")

    op.execute("ALTER TABLE users ALTER COLUMN id TYPE INTEGER USING id::integer")
    op.alter_column('users', 'id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default="nextval('users_id_seq'::regclass)")

    op.execute("ALTER TABLE admin ALTER COLUMN id TYPE INTEGER USING id::integer")
    op.alter_column('admin', 'id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True
    )

    # Step 2: Alter referencing fields
    op.execute("ALTER TABLE users ALTER COLUMN organization_id TYPE INTEGER USING organization_id::integer")
    op.alter_column('users', 'organization_id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=True)

    op.execute("ALTER TABLE users ALTER COLUMN assigned_staff_id TYPE INTEGER USING assigned_staff_id::integer")
    op.alter_column('users', 'assigned_staff_id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=True)

    op.execute("ALTER TABLE org_members ALTER COLUMN id TYPE INTEGER USING id::integer")
    op.alter_column('org_members', 'id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True)

    op.execute("ALTER TABLE org_members ALTER COLUMN user_id TYPE INTEGER USING user_id::integer")
    op.alter_column('org_members', 'user_id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=True)

    op.execute("ALTER TABLE org_members ALTER COLUMN organization_id TYPE INTEGER USING organization_id::integer")
    op.alter_column('org_members', 'organization_id',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=True)

    # ✅ Recreate foreign key constraints AFTER all type changes
    op.create_foreign_key(
        'users_organization_id_fkey',
        'users', 'organizations',
        ['organization_id'], ['id']
    )
    op.create_foreign_key(
        'users_assigned_staff_id_fkey',
        'users', 'org_members',
        ['assigned_staff_id'], ['id']
    )
    op.create_foreign_key(
        'org_members_user_id_fkey',
        'org_members', 'users',
        ['user_id'], ['id']
    )
    op.create_foreign_key(
        'org_members_organization_id_fkey',
        'org_members', 'organizations',
        ['organization_id'], ['id']
    )

def downgrade() -> None:
    # Drop foreign key constraints before reverting column types
    op.drop_constraint('users_assigned_staff_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('org_members_user_id_fkey', 'org_members', type_='foreignkey')

    op.alter_column('users', 'assigned_staff_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('users', 'organization_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('users', 'id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default="nextval('users_id_seq'::regclass")
    op.alter_column('organizations', 'id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default="nextval('organizations_id_seq'::regclass")
    op.alter_column('org_members', 'organization_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('org_members', 'user_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('org_members', 'id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('admin', 'id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True)

    # Re-create foreign key constraints after reverting types
    op.create_foreign_key(
        'org_members_user_id_fkey',
        'org_members', 'users',
        ['user_id'], ['id']
    )
    op.create_foreign_key(
        'users_assigned_staff_id_fkey',
        'users', 'org_members',
        ['assigned_staff_id'], ['id']
    )
    # ### end Alembic commands ###
