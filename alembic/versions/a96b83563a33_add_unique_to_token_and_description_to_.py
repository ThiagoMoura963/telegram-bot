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
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('agents', schema='app')]

    if 'description' not in columns:
        op.add_column('agents', sa.Column('description', sa.Text()), schema='app')

    if 'telegram_token' not in columns:
        op.add_column('agents', sa.Column('telegram_token', sa.Text()), schema='app')

    constraints = [c['name'] for c in inspector.get_unique_constraints('agents', schema='app')]
    if 'uq_agents_telegram_token' not in constraints:
        op.create_unique_constraint('uq_agents_telegram_token', 'agents', ['telegram_token'], schema='app')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_agents_telegram_token', 'agents', schema='app', type_='unique')
    op.drop_column('agents', 'telegram_token', schema='app')
    op.drop_column('agents', 'description', schema='app')
