"""Extend products table

Revision ID: 339ae1d46633
Revises: c24977d3e617
Create Date: 2025-01-08 00:03:45.808633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '339ae1d46633'
down_revision: Union[str, None] = 'c24977d3e617'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('quantity', sa.Integer(), nullable=True))
    op.add_column('product', sa.Column('characteristics', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'characteristics')
    op.drop_column('product', 'quantity')
    # ### end Alembic commands ###
