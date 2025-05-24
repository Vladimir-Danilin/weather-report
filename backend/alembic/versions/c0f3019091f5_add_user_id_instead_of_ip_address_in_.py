"""Add user_id instead of ip_address in UserQuery

Revision ID: c0f3019091f5
Revises: 41c25d58400a
Create Date: 2025-05-25 01:26:19.726911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0f3019091f5'
down_revision: Union[str, None] = '41c25d58400a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('user_queries', 'ip_address')
    op.add_column('user_queries', sa.Column('user_id', sa.String(), nullable=False))


def downgrade():
    op.drop_column('user_queries', 'user_id')
    op.add_column('user_queries', sa.Column('ip_address', sa.String(), nullable=True))

