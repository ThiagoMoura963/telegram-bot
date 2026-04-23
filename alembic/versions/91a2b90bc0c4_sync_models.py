"""sync_models

Revision ID: 91a2b90bc0c4
Revises: af30697a6297
Create Date: 2026-04-12 16:10:03.807266

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '91a2b90bc0c4'
down_revision: Union[str, Sequence[str], None] = '56c65e18b783'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('document_chunks', sa.Column('agent_id', postgresql.UUID(as_uuid=True), nullable=False), schema='app')

    op.create_foreign_key(
        'fk_document_chunks_agent',
        'document_chunks',
        'agents',
        ['agent_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE',
    )

    op.add_column('document_chunks', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False), schema='app')

    op.create_foreign_key(
        'fk_document_chunks_user',
        'document_chunks',
        'users',
        ['user_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE',
    )

    op.create_index('idx_document_chunks_agent_id', 'document_chunks', ['agent_id'], schema='app')


def downgrade() -> None:
    op.drop_index('idx_document_chunks_agent_id', table_name='document_chunks', schema='app')
    op.drop_constraint('fk_document_chunks_agent', 'document_chunks', schema='app', type_='foreignkey')
    op.drop_column('document_chunks', 'agent_id', schema='app')
