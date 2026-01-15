from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account, Transaction, LedgerEntry, EntryType

router = APIRouter(prefix="/api")


@router.post("/accounts")
def create_account(user_id: str, account_type: str, currency: str, db: Session = Depends(get_db)):
    account = Account(
        user_id=user_id,
        account_type=account_type,
        currency=currency
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.post("/transactions")
def create_transaction(reference: str, db: Session = Depends(get_db)):
    txn = Transaction(reference=reference)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


@router.post("/ledger-entry")
def create_ledger_entry(
    transaction_id: int,
    account_id: int,
    amount: float,
    entry_type: EntryType,
    db: Session = Depends(get_db)
):
    entry = LedgerEntry(
        transaction_id=transaction_id,
        account_id=account_id,
        amount=amount,
        entry_type=entry_type
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
