"""alter hotel name column

Revision ID: 2437c49f3640
Revises: 3aed2b7a8e37
Create Date: 2018-09-03 09:12:40.740971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2437c49f3640'
down_revision = '3aed2b7a8e37'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='hotels',
        column_name='name',
        existing_type=sa.String(length=100),
        existing_nullable=True,
        existing_server_default=None,
        type_=sa.String(length=256),
    )
    pass


def downgrade():
    op.alter_column(
        table_name='hotels',
        column_name='name',
        existing_type=sa.String(length=256),
        existing_nullable=True,
        existing_server_default=None,
        type_=sa.String(length=100),
    )
    pass
