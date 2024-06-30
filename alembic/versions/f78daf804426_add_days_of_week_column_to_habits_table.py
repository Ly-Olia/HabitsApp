"""Add days_of_week column to habits table

Revision ID: f78daf804426
Revises: ac7655fcd6dc
Create Date: 2024-05-06 17:31:36.392077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f78daf804426'
down_revision: Union[str, None] = 'ac7655fcd6dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column('todos', sa.Column('days_of_week', sa.ARRAY(sa.Integer), nullable=True))

def downgrade():

    op.add_column('todos', sa.Column('days_of_week', sa.String, nullable=True))
