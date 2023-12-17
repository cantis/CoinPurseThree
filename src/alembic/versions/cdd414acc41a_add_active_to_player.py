"""Add active to player

Revision ID: cdd414acc41a
Revises: f1fdd02368ab
Create Date: 2023-12-16 22:36:40.434882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdd414acc41a'
down_revision: Union[str, None] = 'f1fdd02368ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('isActive', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('players', 'isActive')
    # ### end Alembic commands ###
