from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.database import get_db
from app.models import Account, Transaction, LedgerEntry, EntryType

router = APIRouter(prefix="/api")


# -------------------- ACCOUNT --------------------
@router.post("/accounts")
def create_account(user_id: str, currency: str, db: Session = Depends(get_db)):
    acc = Account(user_id=user_id, currency=currency)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc


# -------------------- BALANCE --------------------
def get_balance(db: Session, account_id: int):
    credits = db.scalar(
        select(func.coalesce(func.sum(LedgerEntry.amount), 0))
        .where(LedgerEntry.account_id == account_id)
        .where(LedgerEntry.entry_type == EntryType.credit)
    )

    debits = db.scalar(
        select(func.coalesce(func.sum(LedgerEntry.amount), 0))
        .where(LedgerEntry.account_id == account_id)
        .where(LedgerEntry.entry_type == EntryType.debit)
    )

    return credits - debits


@router.get("/accounts/{account_id}/balance")
def balance(account_id: int, db: Session = Depends(get_db)):
    return {"balance": float(get_balance(db, account_id))}


# -------------------- TRANSFER --------------------
@router.post("/transfer")
def transfer(
    from_account_id: int,
    to_account_id: int,
    amount: float,
    reference: str,
    db: Session = Depends(get_db),
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    try:
        with db.begin():
            # Lock rows (prevents race conditions)
            from_acc = db.execute(
                select(Account).where(Account.id == from_account_id).with_for_update()
            ).scalar_one()

            to_acc = db.execute(
                select(Account).where(Account.id == to_account_id).with_for_update()
            ).scalar_one()

            balance = get_balance(db, from_account_id)
            if balance < amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")

            txn = Transaction(reference=reference)
            db.add(txn)
            db.flush()

            db.add_all([
                LedgerEntry(
                    transaction_id=txn.id,
                    account_id=from_account_id,
                    amount=amount,
                    entry_type=EntryType.debit,
                ),
                LedgerEntry(
                    transaction_id=txn.id,
                    account_id=to_account_id,
                    amount=amount,
                    entry_type=EntryType.credit,
                )
            ])

        return {"status": "success", "transaction_id": txn.id}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Transfer failed")


# -------------------- HISTORY --------------------
@router.get("/accounts/{account_id}/ledger")
def ledger(account_id: int, db: Session = Depends(get_db)):
    entries = db.query(LedgerEntry).filter_by(account_id=account_id).all()
    return entries
