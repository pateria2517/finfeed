"""initial application tables

Revision ID: 001_initial
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("identifier", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="user"),
        sa.Column("mode", sa.String(length=20), nullable=False, server_default="P1_RETAIL"),
        sa.Column("persona", sa.JSON(), nullable=False),
        sa.Column("interests", sa.JSON(), nullable=False),
        sa.Column("holdings", sa.JSON(), nullable=False),
        sa.Column("feedback", sa.JSON(), nullable=False),
    )
    op.create_index("ix_users_identifier", "users", ["identifier"], unique=True)


def downgrade():
    op.drop_index("ix_users_identifier", table_name="users")
    op.drop_table("users")
