"""add agent_id to document_chunks

Revision ID: f56459a7eaaa
Revises: 56c65e18b783
Create Date: 2026-04-18 19:00:16.489162

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'f56459a7eaaa'
down_revision: Union[str, Sequence[str], None] = '91a2b90bc0c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
