from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class EntryType(str, enum.Enum):
    debit = "debit"
    credit = "credit"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    account_type = Column(String)
    currency = Column(String)

    ledger_entries = relationship("LedgerEntry", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    ledger_entries = relationship("LedgerEntry", back_populates="transaction")


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))

    amount = Column(Numeric(12, 2))
    entry_type = Column(Enum(EntryType))
    timestamp = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="ledger_entries")
    transaction = relationship("Transaction", back_populates="ledger_entries")
