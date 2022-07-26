"""Initialize community entity

Revision ID: 6c3c435b27d6
Revises:
Create Date: 2022-07-24 21:18:30.015087

"""
import time
from alembic import op
import sqlalchemy as sa

from app.dependency import Authority
from app.hashing import Hash


# revision identifiers, used by Alembic.
revision = '6c3c435b27d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('''
                INSERT INTO users (id, nickname, email, password, authority, created_at)
                VALUES (1, 'admin', 'admin', '{0}', 'GOD', {1}); '''.format(Hash.bcrypt('admin'), int(time.time())))


def downgrade() -> None:
    op.execute('''
                DELETE FROM users WHERE ("id" = "1")
    ''')
