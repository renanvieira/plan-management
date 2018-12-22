"""create_exercise_table

Revision ID: 913db5a6b9da
Revises: cc7d06c15b1a
Create Date: 2018-12-22 04:05:19.334117

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = '913db5a6b9da'
down_revision = 'cc7d06c15b1a'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_table("exercises",
                    sa.Column("id",
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column("day_id",
                              sa.Integer),
                    sa.Column("name",
                              sa.String(64),
                              nullable=False),
                    sa.Column("reps",
                              sa.Integer,
                              nullable=False),
                    sa.Column("sets",
                              sa.Integer,
                              nullable=False),
                    sa.Column("created_at",
                              sa.DateTime,
                              nullable=False, server_default=func.current_timestamp()),
                    sa.Column("updated_at",
                              sa.DateTime,
                              nullable=True)

                    )

    op.create_foreign_key(
        None,
        'exercises',
        'days',
        ['day_id'], ['id'],
    )


def downgrade():
    op.drop_table("exercises")
