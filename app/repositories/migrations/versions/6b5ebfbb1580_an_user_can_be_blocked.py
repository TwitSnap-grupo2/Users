"""An user can be blocked

Revision ID: 6b5ebfbb1580
Revises: 4294e617d57a
Create Date: 2024-11-22 09:48:23.710578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b5ebfbb1580'
down_revision: Union[str, None] = '4294e617d57a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_blocked', sa.Boolean(), server_default='False', nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_blocked')
    # ### end Alembic commands ###
