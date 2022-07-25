"""Initialize community entity

Revision ID: 6c3c435b27d6
Revises:
Create Date: 2022-07-24 21:18:30.015087

"""
from alembic import op
import sqlalchemy as sa

from app.dependency import Authority


# revision identifiers, used by Alembic.
revision = '6c3c435b27d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False,
                              primary_key=True),
                    sa.Column('nickname', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('authority', sa.Enum(Authority), nullable=False),
                    sa.Column('created_at', sa.BigInteger(), nullable=False))


def downgrade() -> None:
    op.drop_table('users')
