 # type: ignore

"""create_documents_table

Revision ID: 33b1beea550c
Revises: 
Create Date: 2026-03-10 15:16:53.657034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '33b1beea550c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # extensões necessárias
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # schema
    op.execute("CREATE SCHEMA IF NOT EXISTS app")

    # tabela documents
    op.create_table(
        "documents",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("file_name", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        schema="app"
    )

    #tabela document_chunks
    op.create_table(
        "document_chunks",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("app.documents.id"),
            nullable=False
        ),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("content_vector", Vector(1536), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()")
        ),
        schema="app"
    )

    # índice HNSW do pgvector
    op.execute("""
        CREATE INDEX document_chunks_content_vector_hnsw_idx
        ON app.document_chunks
        USING hnsw (content_vector vector_cosine_ops)
        WITH (m='16', ef_construction='64')
    """)




def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS app.document_chunks_content_vector_hnsw_idx")

    op.drop_table("document_chunks", schema="app")
    op.drop_table("documents", schema="app")
