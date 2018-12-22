"""create_plan_table

Revision ID: 2cb5d88827bc
Revises: e90700904e77
Create Date: 2018-12-22 03:53:33.905945

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = '2cb5d88827bc'
down_revision = 'e90700904e77'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_table("plans",
                    sa.Column("id",
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column("name",
                              sa.String(64),
                              nullable=False),
                    sa.Column("created_at",
                              sa.DateTime,
                              nullable=False, server_default=func.current_timestamp()),
                    sa.Column("updated_at",
                              sa.DateTime,
                              nullable=True),
                    sa.Column("deleted_at",
                              sa.DateTime,
                              nullable=True)
                    )


def downgrade():
    op.drop_table("plans")
