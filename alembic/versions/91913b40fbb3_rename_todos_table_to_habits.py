"""Rename todos table to habits

Revision ID: 91913b40fbb3
Revises: f78daf804426
Create Date: 2024-05-10 16:40:31.718245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '91913b40fbb3'
down_revision: Union[str, None] = 'f78daf804426'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('todos', 'habits')


def downgrade() -> None:
    op.rename_table('habits', 'todos')
