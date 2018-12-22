"""create_users_table

Revision ID: e90700904e77
Revises: 
Create Date: 2018-12-22 03:47:05.812085

"""
import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.sql.functions import func

revision = 'e90700904e77'
down_revision = None
branch_labels = ('default',)
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id",
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column("first_name",
                              sa.String(64),
                              nullable=False),
                    sa.Column("last_name",
                              sa.String(64),
                              nullable=False),
                    sa.Column("email",
                              sa.String(320),
                              nullable=False),
                    sa.Column("birth_date",
                              sa.Date,
                              nullable=False),
                    sa.Column("password",
                              sa.Binary(60),
                              nullable=True),
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
    op.drop_table("users")
