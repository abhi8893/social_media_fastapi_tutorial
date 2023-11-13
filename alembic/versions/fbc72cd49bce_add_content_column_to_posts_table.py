"""add content column to posts table

Revision ID: fbc72cd49bce
Revises: 8efe050a0aff
Create Date: 2023-11-09 11:11:28.583196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbc72cd49bce'
down_revision: Union[str, None] = '8efe050a0aff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
