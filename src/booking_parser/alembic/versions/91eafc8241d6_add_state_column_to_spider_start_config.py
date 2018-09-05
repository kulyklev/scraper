"""add state column to spider start config

Revision ID: 91eafc8241d6
Revises: 0b649eb0586f
Create Date: 2018-09-05 12:10:50.659124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91eafc8241d6'
down_revision = '0b649eb0586f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'spider_start_config',
        sa.Column('state', sa.SmallInteger, comment='1 - pause, 2 - resume, 3 - stop, other values - run', default=0)
    )
    pass


def downgrade():
    op.drop_column(
        'spider_start_config',
        'state'
    )
    pass
