"""add revoked_at and indexes to refresh_tokens

Revision ID: 0aa60466774f
Revises: 53bc1136df96
Create Date: 2025-05-24 21:45:54.701255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0aa60466774f'
down_revision: Union[str, None] = '53bc1136df96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_tokens', sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_constraint('refresh_tokens_jti_key', 'refresh_tokens', type_='unique')
    op.create_index(op.f('ix_refresh_tokens_expires_at'), 'refresh_tokens', ['expires_at'], unique=False)
    op.create_index(op.f('ix_refresh_tokens_jti'), 'refresh_tokens', ['jti'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_refresh_tokens_jti'), table_name='refresh_tokens')
    op.drop_index(op.f('ix_refresh_tokens_expires_at'), table_name='refresh_tokens')
    op.create_unique_constraint('refresh_tokens_jti_key', 'refresh_tokens', ['jti'])
    op.drop_column('refresh_tokens', 'revoked_at')
    # ### end Alembic commands ###
