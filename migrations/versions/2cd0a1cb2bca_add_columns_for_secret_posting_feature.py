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

    op.execute("UPDATE postings SET is_locked = 1")
    # op.alter_column('postings', 'is_locked', nullable=False)


# WHY
# https://www.techonthenet.com/sqlite/tables/alter_table.php
# 'Drop column in table'
def downgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name not in ['sqlite']:
        op.drop_column('postings', 'is_locked')
        op.drop_column('postings', 'password')
        return

    op.rename_table('postings', '_postings')
    op.create_table('postings',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=128), nullable=True),
                    sa.Column('body', sa.String(), nullable=False),
                    sa.Column('published_at', sa.BigInteger(), nullable=False),
                    sa.Column('updated_at', sa.BigInteger(), nullable=False),
                    sa.Column('community_id', sa.Integer(),
                              sa.ForeignKey("communities.id")),
                    sa.Column('user_id', sa.Integer(),
                              sa.ForeignKey("users.id")),
                    sa.PrimaryKeyConstraint('id'))
    op.execute('''
        INSERT INTO postings (id, title, body, published_at, updated_at, community_id, user_id)
        SELECT id, title, body, published_at, updated_at, community_id, user_id
        FROM _postings;''')
    op.drop_table("_postings")
