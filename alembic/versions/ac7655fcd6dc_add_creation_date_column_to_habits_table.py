"""Add creation_date column to habits table

Revision ID: ac7655fcd6dc
Revises: 
Create Date: 2024-05-04 19:26:57.006231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ac7655fcd6dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the new column with the Date data type to the todos table
    op.add_column('todos', sa.Column('creation_date', sa.Date))


def downgrade():
    # Remove the column if rolling back the migration
    op.drop_column('todos', 'creation_date')
