"""create documents table

Revision ID: 02efdd7ddf94
Revises:
Create Date: 2026-03-29 18:53:15.182083

"""

from typing import Sequence, Union

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '02efdd7ddf94'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # extensões necessárias
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto" SCHEMA public')
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector" SCHEMA public')

    # schema
    op.execute('CREATE SCHEMA IF NOT EXISTS app')

    # tabela documents
    op.create_table(
        'documents',
        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),
        sa.Column('file_name', sa.Text(), nullable=False),
        sa.Column(
            'agent_id',
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        schema='app',
    )

    # tabela document_chunks
    op.create_table(
        'document_chunks',
        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),
        sa.Column(
            'document_id',
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('app.documents.id', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('content_vector', Vector(1536), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        schema='app',
    )

    # índice HNSW do pgvector
    op.execute("""
        CREATE INDEX document_chunks_content_vector_hnsw_idx
        ON app.document_chunks
        USING hnsw (content_vector vector_cosine_ops)
        WITH (m='16', ef_construction='64')
    """)
#
# def downgrade() -> None:
#    """Downgrade schema."""
#    op.execute('DROP INDEX IF EXISTS app.document_chunks_content_vector_hnsw_idx')
#    op.drop_constraint('fk_documents_agent', 'documents', schema='app', type_='foreignkey')
#    op.drop_table('agents', schema='app')
#
#   op.drop_table('document_chunks', schema='app')
#    op.drop_table('documents', schema='app')
