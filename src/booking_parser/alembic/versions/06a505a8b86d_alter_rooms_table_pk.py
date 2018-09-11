"""alter rooms table pk

Revision ID: 06a505a8b86d
Revises: 52d8530f8001
Create Date: 2018-09-11 09:13:01.372762

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


# revision identifiers, used by Alembic.
revision = '06a505a8b86d'
down_revision = '52d8530f8001'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(
        table_name='rooms',
        column_name='id'
    )

    op.create_primary_key(
        "PRIMARY KEY", "rooms",
        ["room_type_id", "date", "sleeps"]
    )

    pass


def downgrade():
    op.drop_constraint(
        constraint_name="rooms_ibfk_1",
        table_name="rooms",
        type_="foreignkey"
    )

    op.drop_constraint(
        constraint_name="PRIMARY KEY",
        table_name="rooms",
        type_="primary"
    )

    op.execute("ALTER TABLE rooms ADD COLUMN id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")

    op.create_foreign_key(
        constraint_name="rooms_ibfk_1",
        source_table="rooms",
        referent_table="room_types",
        local_cols=["room_type_id"],
        remote_cols=["id"]
    )
    pass
