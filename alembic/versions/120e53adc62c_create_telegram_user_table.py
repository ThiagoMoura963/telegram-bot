"""create telegram_users table

Revision ID: c4g5h6i7j8k9
Revises: b3f1c2d4e5a6
Create Date: 2026-05-06 23:45:00.000000

"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql # Importante para o UUID
from alembic import op

revision: str = 'c4g5h6i7j8k9'
down_revision: Union[str, Sequence[str], None] = 'b3f1c2d4e5a6'

def upgrade() -> None:
    op.create_table(
        'telegram_users',
        sa.Column(
            'id', 
            postgresql.UUID(as_uuid=True), 
            primary_key=True, 
            server_default=sa.text('gen_random_uuid()'),
            nullable=False
        ),
        sa.Column(
            'telegram_id', 
            sa.BigInteger(), 
            unique=True,
            nullable=False
        ),
        sa.Column('first_name', sa.String(length=255), nullable=True),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        schema='app',
    )

    op.create_index(
        'idx_telegram_users_tg_id',
        'telegram_users',
        ['telegram_id'],
        schema='app',
    )

def downgrade() -> None:
    op.drop_index('idx_telegram_users_tg_id', table_name='telegram_users', schema='app')
    op.drop_table('telegram_users', schema='app')