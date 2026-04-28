"""add_unique_to_token_and_description_to_agent

Revision ID: a96b83563a33
Revises: 2ce84d3d9c85
Create Date: 2026-04-27 22:44:50.678195

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a96b83563a33'
down_revision: Union[str, Sequence[str], None] = '2ce84d3d9c85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('agents', sa.Column('description', sa.Text()), schema='app')
    op.create_unique_constraint('uq_agents_telegram_token', 'agents', ['telegram_token'], schema='app')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_agents_telegram_token', 'agents', schema='app', type_='unique')
    op.drop_column('agents', 'description', schema='app')
