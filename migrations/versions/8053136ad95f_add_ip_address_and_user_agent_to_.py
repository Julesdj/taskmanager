"""Add ip_address and user_agent to refresh_tokens

Revision ID: 8053136ad95f
Revises: 0aa60466774f
Create Date: 2025-05-25 10:14:37.285959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8053136ad95f'
down_revision: Union[str, None] = '0aa60466774f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
