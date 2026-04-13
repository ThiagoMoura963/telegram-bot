"""sync_models

Revision ID: 91a2b90bc0c4
Revises: af30697a6297
Create Date: 2026-04-12 16:10:03.807266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91a2b90bc0c4'
down_revision: Union[str, Sequence[str], None] = 'af30697a6297'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
