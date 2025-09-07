"""Create designs table

Revision ID: 002
Revises: 001
Create Date: 2025-01-05 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create designs table
    op.create_table('designs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('prompt_config', sa.JSON(), nullable=False),
        sa.Column('html_code', sa.Text(), nullable=True),
        sa.Column('css_classes', sa.Text(), nullable=True),
        sa.Column('javascript', sa.Text(), nullable=True),
        sa.Column('images', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_designs_user_id'), 'designs', ['user_id'], unique=False)
    op.create_index(op.f('ix_designs_status'), 'designs', ['status'], unique=False)
    op.create_index(op.f('ix_designs_is_public'), 'designs', ['is_public'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_designs_is_public'), table_name='designs')
    op.drop_index(op.f('ix_designs_status'), table_name='designs')
    op.drop_index(op.f('ix_designs_user_id'), table_name='designs')
    op.drop_table('designs')
