"""create_plans_users_table

Revision ID: 4db90dc1993e
Revises: 2cb5d88827bc
Create Date: 2018-12-22 03:54:54.675587

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4db90dc1993e'
down_revision = '2cb5d88827bc'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_table("plans_users",
                    sa.Column("id",
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column("plan_id",
                              sa.Integer,
                              nullable=False),
                    sa.Column("user_id",
                              sa.Integer,
                              nullable=False)
                    )

    op.create_foreign_key(
        None,
        'plans_users',
        'users',
        ['user_id'], ['id'],
    )

    op.create_foreign_key(
        None,
        'plans_users',
        'plans',
        ['plan_id'], ['id'],
    )


def downgrade():
    op.drop_table("plans_users")
