"""alter_nullables_spider_start_config

Revision ID: 52d8530f8001
Revises: ee0a2d1104f1
Create Date: 2018-09-06 16:53:51.253367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52d8530f8001'
down_revision = 'ee0a2d1104f1'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='spider_start_config',
        column_name='country',
        existing_type=sa.String(length=100),
        existing_nullable=True,
        existing_server_default=None,
        nullable=False,
    )

    op.alter_column(
        table_name='spider_start_config',
        column_name='city',
        existing_type=sa.String(length=100),
        existing_nullable=True,
        existing_server_default=None,
        nullable=False,
    )

    op.alter_column(
        table_name='spider_start_config',
        column_name='checkin_date',
        existing_type=sa.Date,
        existing_nullable=True,
        existing_server_default=None,
        nullable=False,
    )

    op.alter_column(
        table_name='spider_start_config',
        column_name='checkout_date',
        existing_type=sa.Date,
        existing_nullable=True,
        existing_server_default=None,
        nullable=False,
    )
    pass


def downgrade():
    op.alter_column(
        table_name='spider_start_config',
        column_name='country',
        existing_type=sa.String(length=100),
        existing_nullable=False,
        existing_server_default=None,
        nullable=True,
    )

    op.alter_column(
        table_name='spider_start_config',
        column_name='city',
        existing_type=sa.String(length=100),
        existing_nullable=False,
        existing_server_default=None,
        nullable=True,
    )

    op.alter_column(
        table_name='spider_start_config',
        column_name='checkin_date',
        existing_type=sa.Date,
        existing_nullable=False,
        existing_server_default=None,
        nullable=True,
    )

    op.alter_column(
        table_name='spider_start_config',
        column_name='checkout_date',
        existing_type=sa.Date,
        existing_nullable=False,
        existing_server_default=None,
        nullable=True,
    )
    pass
