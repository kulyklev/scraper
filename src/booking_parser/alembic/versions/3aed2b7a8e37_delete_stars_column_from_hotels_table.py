"""delete stars column from hotels table

Revision ID: 3aed2b7a8e37
Revises: a8e03c865b08
Create Date: 2018-08-31 11:23:39.211892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aed2b7a8e37'
down_revision = 'a8e03c865b08'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(
        'hotels',
        'stars',
    )
    pass


def downgrade():
    op.add_column(
        'hotels',
        sa.Column('stars', sa.SmallInteger),
    )
    pass
