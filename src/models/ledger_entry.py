from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from database import Base


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey('accounts.id', ondelete='RESTRICT'),
        nullable=False,
        index=True
    )
    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey('transactions.id', ondelete='RESTRICT'),
        nullable=False,
        index=True
    )
    entry_type = Column(String(10), nullable=False)
    amount = Column(Numeric(19, 4), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    account = relationship("Account", lazy="joined")
    transaction = relationship("Transaction", lazy="joined")
    
    def __repr__(self):
        return f"<LedgerEntry(id={self.id}, type={self.entry_type}, amount={self.amount})>"
