"""link chunks to documents with cascade

Revision ID: 2ce84d3d9c85
Revises: f56459a7eaaa
Create Date: 2026-04-18 19:08:45.429634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ce84d3d9c85'
down_revision: Union[str, Sequence[str], None] = 'f56459a7eaaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        'fk_document_chunks_document',
        'document_chunks',
        'documents',
        ['document_id'],
        ['id'],
        source_schema='app',
        referent_schema='app',
        ondelete='CASCADE'
    )

    op.create_index(
        'idx_chunks_document_id',
        'document_chunks',
        ['document_id'],
        schema='app'
    )

def downgrade() -> None:
    op.drop_index('idx_chunks_document_id', table_name='document_chunks', schema='app')
    op.drop_constraint('fk_document_chunks_document', 'document_chunks', schema='app', type_='foreignkey')
    op.drop_column('document_chunks', 'document_id', schema='app')
