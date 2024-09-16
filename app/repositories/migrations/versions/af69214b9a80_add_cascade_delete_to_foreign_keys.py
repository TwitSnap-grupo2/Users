"""Add cascade delete to foreign keys

Revision ID: af69214b9a80
Revises: 55e6fe16b610
Create Date: 2024-09-16 18:38:01.368465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af69214b9a80'
down_revision: Union[str, None] = '55e6fe16b610'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_goals_id_user_fkey', 'users_goals', type_='foreignkey')
    op.create_foreign_key(None, 'users_goals', 'users', ['id_user'], ['id'], ondelete='CASCADE')
    op.drop_constraint('users_interests_id_user_fkey', 'users_interests', type_='foreignkey')
    op.create_foreign_key(None, 'users_interests', 'users', ['id_user'], ['id'], ondelete='CASCADE')
    op.drop_constraint('users_twitsnaps_id_user_fkey', 'users_twitsnaps', type_='foreignkey')
    op.create_foreign_key(None, 'users_twitsnaps', 'users', ['id_user'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_twitsnaps', type_='foreignkey')
    op.create_foreign_key('users_twitsnaps_id_user_fkey', 'users_twitsnaps', 'users', ['id_user'], ['id'])
    op.drop_constraint(None, 'users_interests', type_='foreignkey')
    op.create_foreign_key('users_interests_id_user_fkey', 'users_interests', 'users', ['id_user'], ['id'])
    op.drop_constraint(None, 'users_goals', type_='foreignkey')
    op.create_foreign_key('users_goals_id_user_fkey', 'users_goals', 'users', ['id_user'], ['id'])
    # ### end Alembic commands ###