"""create room types table

Revision ID: b315a7a349a4
Revises: 5cc0c9da2212
Create Date: 2018-08-30 10:11:11.403480

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER



# revision identifiers, used by Alembic.
revision = 'b315a7a349a4'
down_revision = '5cc0c9da2212'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'room_types',
        sa.Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=False, nullable=False),
        sa.Column('hotel_id', INTEGER(unsigned=True), ForeignKey('hotels.id'), nullable=False),
        sa.Column('type', sa.String(300)),
        sa.Column('photo', sa.String(100)),
    )
    pass


def downgrade():
    op.drop_table('room_types')
    pass
