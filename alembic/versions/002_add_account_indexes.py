"""Add performance indexes

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add index for account status lookups
    op.create_index('idx_accounts_status', 'accounts', ['status'], unique=False)
    
    # Add index for filtering accounts by type and status
    op.create_index('idx_accounts_type_status', 'accounts', ['account_type', 'status'], unique=False)
    
    # Add index for ledger entries by account and date
    op.create_index('idx_ledger_account_date', 'ledger_entries', ['account_id', 'created_at'], unique=False)
    
    # Add index for transaction search by date range
    op.create_index('idx_transactions_completed_at', 'transactions', ['completed_at'], unique=False)
    
    # Add index for transactions by type and status
    op.create_index('idx_transactions_type_status', 'transactions', ['type', 'status'], unique=False)
    
    # Add partial index for active accounts only
    op.execute("""
        CREATE INDEX idx_accounts_active 
        ON accounts(status) 
        WHERE status = 'active';
    """)
    
    # Add partial index for completed transactions
    op.execute("""
        CREATE INDEX idx_transactions_completed 
        ON transactions(status) 
        WHERE status = 'completed';
    """)


def downgrade() -> None:
    # Drop partial indexes
    op.execute("DROP INDEX IF EXISTS idx_transactions_completed;")
    op.execute("DROP INDEX IF EXISTS idx_accounts_active;")
    
    # Drop regular indexes
    op.drop_index('idx_transactions_type_status', table_name='transactions')
    op.drop_index('idx_transactions_completed_at', table_name='transactions')
    op.drop_index('idx_ledger_account_date', table_name='ledger_entries')
    op.drop_index('idx_accounts_type_status', table_name='accounts')
    op.drop_index('idx_accounts_status', table_name='accounts')
