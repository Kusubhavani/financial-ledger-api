import pytest
from decimal import Decimal
import uuid
from datetime import datetime

from models.account import Account
from models.transaction import Transaction
from models.ledger_entry import LedgerEntry

def test_account_model():
    """Test Account model creation"""
    account = Account(
        user_id="test_user_123",
        account_type="checking",
        currency="USD",
        status="active"
    )
    
    assert account.user_id == "test_user_123"
    assert account.account_type == "checking"
    assert account.currency == "USD"
    assert account.status == "active"
    assert account.id is not None
    assert isinstance(account.id, uuid.UUID)

def test_account_model_validation():
    """Test Account model validation"""
    with pytest.raises(Exception):
        Account(
            user_id="test_user",
            account_type="invalid_type",  # Invalid type
            currency="USD"
        )
    
    with pytest.raises(Exception):
        Account(
            user_id="test_user",
            account_type="checking",
            currency="USDD",  # Invalid currency
            status="invalid_status"  # Invalid status
        )

def test_transaction_model():
    """Test Transaction model creation"""
    transaction = Transaction(
        type="transfer",
        amount=Decimal("100.50"),
        currency="USD",
        description="Test transaction",
        status="pending"
    )
    
    assert transaction.type == "transfer"
    assert transaction.amount == Decimal("100.50")
    assert transaction.currency == "USD"
    assert transaction.description == "Test transaction"
    assert transaction.status == "pending"
    assert transaction.id is not None

def test_transaction_model_validation():
    """Test Transaction model validation"""
    with pytest.raises(Exception):
        Transaction(
            type="invalid_type",
            amount=Decimal("100.50"),
            currency="USD"
        )
    
    with pytest.raises(Exception):
        Transaction(
            type="transfer",
            amount=Decimal("-100.50"),  # Negative amount
            currency="USD"
        )

def test_ledger_entry_model():
    """Test LedgerEntry model creation"""
    account_id = uuid.uuid4()
    transaction_id = uuid.uuid4()
    
    ledger_entry = LedgerEntry(
        account_id=account_id,
        transaction_id=transaction_id,
        entry_type="debit",
        amount=Decimal("100.50")
    )
    
    assert str(ledger_entry.account_id) == str(account_id)
    assert str(ledger_entry.transaction_id) == str(transaction_id)
    assert ledger_entry.entry_type == "debit"
    assert ledger_entry.amount == Decimal("100.50")
    assert ledger_entry.id is not None

def test_ledger_entry_model_validation():
    """Test LedgerEntry model validation"""
    with pytest.raises(Exception):
        LedgerEntry(
            account_id=uuid.uuid4(),
            transaction_id=uuid.uuid4(),
            entry_type="invalid_type",  # Invalid type
            amount=Decimal("100.50")
        )
    
    with pytest.raises(Exception):
        LedgerEntry(
            account_id=uuid.uuid4(),
            transaction_id=uuid.uuid4(),
            entry_type="debit",
            amount=Decimal("-100.50")  # Negative amount
        )

def test_model_relationships(db):
    """Test model relationships"""
    # Create account
    account = Account(
        user_id="test_user",
        account_type="checking",
        currency="USD"
    )
    db.add(account)
    db.commit()
    
    # Create transaction
    transaction = Transaction(
        type="transfer",
        amount=Decimal("100.00"),
        currency="USD"
    )
    db.add(transaction)
    db.commit()
    
    # Create ledger entry
    ledger_entry = LedgerEntry(
        account_id=account.id,
        transaction_id=transaction.id,
        entry_type="debit",
        amount=Decimal("100.00")
    )
    db.add(ledger_entry)
    db.commit()
    
    # Test relationships
    assert ledger_entry.account.id == account.id
    assert ledger_entry.transaction.id == transaction.id
    assert ledger_entry.account.user_id == "test_user"
    assert ledger_entry.transaction.type == "transfer"
