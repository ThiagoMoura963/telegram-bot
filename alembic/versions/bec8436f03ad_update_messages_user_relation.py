# type: ignore

"""update messages user relation

Revision ID: bec8436f03ad
Revises: c4g5h6i7j8k9
Create Date: 2026-05-06 23:59:31.651021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'bec8436f03ad'
down_revision: Union[str, Sequence[str], None] = 'c4g5h6i7j8k9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('fk_messages_user', 'messages', schema='app', type_='foreignkey')

    op.alter_column(
        'messages', 
        'user_id', 
        new_column_name='telegram_user_id', 
        schema='app'
    )

    op.create_foreign_key(
        'fk_messages_telegram_user',
        'messages',
        'telegram_users',
        ['telegram_user_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE'
    )

    op.execute('ALTER INDEX app.idx_messages_agent_user RENAME TO idx_messages_agent_telegram_user')


def downgrade() -> None:
    op.drop_constraint('fk_messages_telegram_user', 'messages', schema='app', type_='foreignkey')
    
    op.alter_column(
        'messages', 
        'telegram_user_id', 
        new_column_name='user_id', 
        schema='app'
    )

    op.create_foreign_key(
        'fk_messages_user',
        'messages',
        'users',
        ['user_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE'
    )
    
    op.execute('ALTER INDEX app.idx_messages_agent_telegram_user RENAME TO idx_messages_agent_user')