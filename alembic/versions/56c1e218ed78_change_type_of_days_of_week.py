"""change type of days_of_week

Revision ID: 56c1e218ed78
Revises: 61880c6e4b58
Create Date: 2024-07-17 15:15:47.082222

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56c1e218ed78"
down_revision: Union[str, None] = "61880c6e4b58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Change column type to ARRAY(Integer)
    op.alter_column(
        "habits",
        "days_of_week",
        existing_type=sa.Integer(),
        type_=sa.ARRAY(sa.Integer),
        existing_nullable=False,
        postgresql_using="ARRAY[days_of_week]::INTEGER[]",
    )


def downgrade():
    # Change column type back to Integer (if needed)
    op.alter_column(
        "habits",
        "days_of_week",
        existing_type=sa.ARRAY(sa.Integer),
        type_=sa.Integer,
        existing_nullable=False,
        postgresql_using="days_of_week[1]",
    )
    # ### end Alembic commands ###
