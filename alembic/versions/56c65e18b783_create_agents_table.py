"""create agents table

Revision ID: 56c65e18b783
Revises: 91a2b90bc0c4
Create Date: 2026-04-16 17:53:25.774841

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '56c65e18b783'
down_revision: Union[str, Sequence[str], None] = 'af30697a6297'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column(
            'user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False
        ),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('system_prompt', sa.Text(), nullable=False),
        sa.Column('api_token', sa.Text(), nullable=False),
        sa.Column('telegram_token', sa.Text(), nullable=False, unique=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        schema='app',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('agents', schema='app')
