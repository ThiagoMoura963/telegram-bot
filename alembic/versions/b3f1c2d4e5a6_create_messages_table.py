"""create messages table

Revision ID: b3f1c2d4e5a6
Revises: a96b83563a33
Create Date: 2026-05-01 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = 'b3f1c2d4e5a6'
down_revision: Union[str, Sequence[str], None] = 'a96b83563a33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'messages',
        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column(
            'user_id',
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            'agent_id',
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('vector_message', Vector(1536)),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        schema='app',
    )

    op.create_foreign_key(
        'fk_messages_user',
        'messages',
        'users',
        ['user_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE',
    )

    op.create_foreign_key(
        'fk_messages_agent',
        'messages',
        'agents',
        ['agent_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE',
    )

    op.create_index(
        'idx_messages_agent_user',
        'messages',
        ['agent_id', 'user_id'],
        schema='app',
    )

    op.create_index(
        'idx_messages_created_at',
        'messages',
        ['created_at'],
        schema='app',
    )

    op.execute("""
        CREATE INDEX idx_messages_vector_hnsw
        ON app.messages
        USING hnsw (vector_message vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
    """)


def downgrade() -> None:
    op.execute('DROP INDEX IF EXISTS app.idx_messages_vector_hnsw')
    op.drop_index('idx_messages_created_at', table_name='messages', schema='app')
    op.drop_index('idx_messages_agent_user', table_name='messages', schema='app')
    op.drop_constraint('fk_messages_agent', 'messages', schema='app', type_='foreignkey')
    op.drop_constraint('fk_messages_user', 'messages', schema='app', type_='foreignkey')
    op.drop_table('messages', schema='app')
