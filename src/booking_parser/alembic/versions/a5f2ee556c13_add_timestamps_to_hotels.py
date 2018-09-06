"""add timestamps to hotels

Revision ID: a5f2ee556c13
Revises: 91eafc8241d6
Create Date: 2018-09-06 15:02:04.884136

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime, func, text, TIMESTAMP

# revision identifiers, used by Alembic.
revision = 'a5f2ee556c13'
down_revision = '91eafc8241d6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'hotels',
        sa.Column('created_at', DateTime, server_default=func.now()),
    )

    op.add_column(
        'hotels',
        sa.Column('updated_at', TIMESTAMP(), nullable=False,
                  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)
    )
    pass


def downgrade():
    op.drop_column(
        'hotels',
        'created_at'
    )

    op.drop_column(
        'hotels',
        'updated_at'
    )
    pass
