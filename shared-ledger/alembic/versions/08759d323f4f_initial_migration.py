"""Initial migration

Revision ID: 08759d323f4f
Revises: 6cd4bbbbe76b
Create Date: 2025-02-03 12:19:16.388568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08759d323f4f'
down_revision: Union[str, None] = '6cd4bbbbe76b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
