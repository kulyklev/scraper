"""add timestamps to room_types

Revision ID: 11a9c73a7d90
Revises: a5f2ee556c13
Create Date: 2018-09-06 15:02:52.152379

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime, func, text, TIMESTAMP

# revision identifiers, used by Alembic.
revision = '11a9c73a7d90'
down_revision = 'a5f2ee556c13'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'room_types',
        sa.Column('created_at', DateTime, server_default=func.now()),
    )

    op.add_column(
        'room_types',
        sa.Column('updated_at', TIMESTAMP(), nullable=False,
                  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), )
    )
    pass


def downgrade():
    op.drop_column(
        'room_types',
        'created_at'
    )

    op.drop_column(
        'room_types',
        'updated_at'
    )
    pass
