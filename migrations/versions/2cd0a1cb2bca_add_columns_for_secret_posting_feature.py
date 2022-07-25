"""add columns for secret posting feature

Revision ID: 2cd0a1cb2bca
Revises: 6c3c435b27d6
Create Date: 2022-07-25 23:03:58.480131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd0a1cb2bca'
down_revision = '6c3c435b27d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postings', sa.Column('is_locked', sa.Boolean()))
    op.add_column('postings', sa.Column('password', sa.String()))


def downgrade() -> None:
    op.drop_column('postings', 'is_locked')
    op.drop_column('postings', 'password')
