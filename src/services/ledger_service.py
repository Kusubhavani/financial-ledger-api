from typing import Optional, List, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import logging

from models.ledger_entry import LedgerEntry
from models.account import Account

logger = logging.getLogger(__name__)


class LedgerService:
    @staticmethod
    def calculate_balance(db: Session, account_id: str) -> Decimal:
        """Calculate current balance by summing ledger entries"""
        try:
            result = db.query(
                func.sum(
                    func.case(
                        (LedgerEntry.entry_type == 'credit', LedgerEntry.amount),
                        (LedgerEntry.entry_type == 'debit', -LedgerEntry.amount),
                        else_=0
                    )
                )
            ).filter(LedgerEntry.account_id == account_id).scalar()
            
            return Decimal(result or 0)
        except Exception as e:
            logger.error(f"Error calculating balance for account {account_id}: {e}")
            return Decimal(0)
    
    @staticmethod
    def get_account_ledger(
        db: Session, 
        account_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[LedgerEntry]:
        """Get chronological ledger entries for an account"""
        try:
            return db.query(LedgerEntry)\
                .filter(LedgerEntry.account_id == account_id)\
                .order_by(LedgerEntry.created_at.desc())\
                .offset(offset)\
                .limit(limit)\
                .all()
        except Exception as e:
            logger.error(f"Error getting ledger for account {account_id}: {e}")
            return []
    
    @staticmethod
    def create_ledger_entries(
        db: Session,
        transaction_id: str,
        debit_account_id: str,
        credit_account_id: str,
        amount: Decimal,
        description: Optional[str] = None
    ) -> Tuple[LedgerEntry, LedgerEntry]:
        """Create balanced debit and credit ledger entries"""
        try:
            # Create debit entry
            debit_entry = LedgerEntry(
                account_id=debit_account_id,
                transaction_id=transaction_id,
                entry_type='debit',
                amount=amount,
            )
            
            # Create credit entry
            credit_entry = LedgerEntry(
                account_id=credit_account_id,
                transaction_id=transaction_id,
                entry_type='credit',
                amount=amount,
            )
            
            db.add(debit_entry)
            db.add(credit_entry)
            db.flush()
            
            logger.info(f"Created ledger entries for transaction {transaction_id}")
            
            return debit_entry, credit_entry
            
        except Exception as e:
            logger.error(f"Error creating ledger entries: {e}")
            raise
    
    @staticmethod
    def verify_double_entry(db: Session, transaction_id: str) -> bool:
        """Verify that a transaction has balanced debit and credit entries"""
        try:
            result = db.query(
                func.sum(
                    func.case(
                        (LedgerEntry.entry_type == 'credit', LedgerEntry.amount),
                        (LedgerEntry.entry_type == 'debit', -LedgerEntry.amount),
                        else_=0
                    )
                )
            ).filter(LedgerEntry.transaction_id == transaction_id).scalar()
            
            return result == 0
        except Exception as e:
            logger.error(f"Error verifying double entry for transaction {transaction_id}: {e}")
            return False
