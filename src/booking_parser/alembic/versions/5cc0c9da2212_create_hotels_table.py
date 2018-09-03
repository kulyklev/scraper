"""create hotels table

Revision ID: 5cc0c9da2212
Revises: 
Create Date: 2018-08-30 10:10:58.684548

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER



# revision identifiers, used by Alembic.
revision = '5cc0c9da2212'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hotels',
        sa.Column('id', INTEGER(unsigned=True), primary_key=True, nullable=False),
        sa.Column('url', sa.VARCHAR(1000)),
        sa.Column('name', sa.String(100)),
        sa.Column('address', sa.String(250)),
        sa.Column('description', sa.Text),
        sa.Column('rate', sa.Float),
        sa.Column('photo', sa.String(100)),
        sa.Column('stars', sa.SmallInteger),
        sa.Index('id_idx', 'id')
    )


def downgrade():
    op.drop_table('hotels')
    pass

