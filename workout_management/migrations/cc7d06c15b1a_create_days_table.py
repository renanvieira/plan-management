"""create_days_table

Revision ID: cc7d06c15b1a
Revises: 4db90dc1993e
Create Date: 2018-12-22 04:03:14.843776

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = 'cc7d06c15b1a'
down_revision = '4db90dc1993e'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_table("days",
                    sa.Column("id",
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column("plan_id",
                              sa.Integer,
                              nullable=False),
                    sa.Column("number",
                              sa.Integer,
                              nullable=False),
                    sa.Column("created_at",
                              sa.DateTime,
                              nullable=False, server_default=func.current_timestamp()),
                    sa.Column("updated_at",
                              sa.DateTime,
                              nullable=True)

                    ),

    op.create_foreign_key(
        None,
        'days',
        'plans',
        ['plan_id'], ['id'],
    )


def downgrade():
    op.drop_table("days")
