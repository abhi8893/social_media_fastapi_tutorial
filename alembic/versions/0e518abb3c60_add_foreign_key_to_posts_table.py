"""add foreign key to posts table

Revision ID: 0e518abb3c60
Revises: c9e240c8aed3
Create Date: 2023-11-09 11:24:05.720206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e518abb3c60'
down_revision: Union[str, None] = 'c9e240c8aed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False)),
    op.create_foreign_key(
        'posts_users_fk', 
        source_table='posts', 
        referent_table='users', 
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
        



def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
