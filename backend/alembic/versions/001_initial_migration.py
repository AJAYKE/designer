"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create designs table
    op.create_table('designs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('thread_id', sa.String(), nullable=False),
        sa.Column('html_code', sa.Text(), nullable=True),
        sa.Column('css_classes', sa.Text(), nullable=True),
        sa.Column('javascript', sa.Text(), nullable=True),
        sa.Column('prompt_config', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('design_plan', sa.Text(), nullable=True),
        sa.Column('images', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('generation_time_ms', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_designs_id', 'designs', ['id'], unique=False)
    op.create_index('ix_designs_thread_id', 'designs', ['thread_id'], unique=True)
    op.create_index('ix_designs_user_id', 'designs', ['user_id'], unique=False)
    op.create_index('ix_designs_session_id', 'designs', ['session_id'], unique=False)
    op.create_index('ix_designs_status', 'designs', ['status'], unique=False)
    op.create_index('ix_designs_created_at', 'designs', ['created_at'], unique=False)

def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_designs_created_at', table_name='designs')
    op.drop_index('ix_designs_status', table_name='designs')
    op.drop_index('ix_designs_session_id', table_name='designs')
    op.drop_index('ix_designs_user_id', table_name='designs')
    op.drop_index('ix_designs_thread_id', table_name='designs')
    op.drop_index('ix_designs_id', table_name='designs')
    
    # Drop table
    op.drop_table('designs')

