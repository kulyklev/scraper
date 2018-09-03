"""create rooms table

Revision ID: a8e03c865b08
Revises: b315a7a349a4
Create Date: 2018-08-30 10:11:17.569822

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER


# revision identifiers, used by Alembic.
revision = 'a8e03c865b08'
down_revision = 'b315a7a349a4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rooms',
        sa.Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('room_type_id', INTEGER(unsigned=True), ForeignKey('room_types.id'), nullable=False),
        sa.Column('price', sa.String(100)),
        sa.Column('date', sa.String(100)),
        sa.Column('sleeps', sa.Integer),
    )
    pass


def downgrade():
    op.drop_table('rooms')
    pass
