"""add timestamps to rooms

Revision ID: ee0a2d1104f1
Revises: 11a9c73a7d90
Create Date: 2018-09-06 15:02:56.398045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime, func, text, TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'ee0a2d1104f1'
down_revision = '11a9c73a7d90'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'rooms',
        sa.Column('created_at', DateTime, server_default=func.now()),
    )

    op.add_column(
        'rooms',
        sa.Column('updated_at', TIMESTAMP(), nullable=False,
                  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), )
    )
    pass


def downgrade():
    op.drop_column(
        'rooms',
        'created_at'
    )

    op.drop_column(
        'rooms',
        'updated_at'
    )
    pass
