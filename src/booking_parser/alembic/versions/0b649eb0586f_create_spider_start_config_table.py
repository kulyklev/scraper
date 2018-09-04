"""create spider start config table

Revision ID: 0b649eb0586f
Revises: 2437c49f3640
Create Date: 2018-09-04 14:11:34.458195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


# revision identifiers, used by Alembic.
revision = '0b649eb0586f'
down_revision = '2437c49f3640'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'spider_start_config',
        sa.Column('id', INTEGER(unsigned=True), primary_key=True, nullable=False),
        sa.Column('country', sa.VARCHAR(128)),
        sa.Column('city', sa.VARCHAR(128)),
        sa.Column('checkin_date', sa.Date),
        sa.Column('checkout_date', sa.Date),
        sa.Column('vpn', sa.Boolean, default=False),
        sa.Column('concurrent_request_amount', sa.SmallInteger),
    )
    pass


def downgrade():
    op.drop_table('spider_start_config')
    pass
