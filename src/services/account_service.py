from typing import List, Optional, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import uuid
import logging

from models.account import Account
from services.ledger_service import LedgerService

logger = logging.getLogger(__name__)


class AccountService:
    @staticmethod
    def create_account(
        db: Session,
        user_id: str,
        account_type: str,
        currency: str = 'USD'
    ) -> Account:
        """Create a new account"""
        try:
            # Validate account type
            valid_types = ['checking', 'savings', 'business']
            if account_type not in valid_types:
                raise ValueError(f"Account type must be one of: {', '.join(valid_types)}")
            
            # Validate currency
            if len(currency) != 3:
                raise ValueError("Currency must be a 3-letter code")
            
            account = Account(
                user_id=user_id,
                account_type=account_type,
                currency=currency.upper(),
                status='active'
            )
            
            db.add(account)
            db.flush()
            
            logger.info(f"Created account {account.id} for user {user_id}")
            
            return account
            
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            raise
    
    @staticmethod
    def get_account(db: Session, account_id: str) -> Optional[Account]:
        """Get account by ID"""
        try:
            return db.query(Account).filter(Account.id == account_id).first()
        except Exception as e:
            logger.error(f"Error getting account {account_id}: {e}")
            return None
    
    @staticmethod
    def get_account_with_balance(db: Session, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account details with calculated balance"""
        try:
            account = AccountService.get_account(db, account_id)
            
            if not account:
                return None
            
            balance = LedgerService.calculate_balance(db, account_id)
            
            return {
                'id': str(account.id),
                'user_id': account.user_id,
                'account_type': account.account_type,
                'currency': account.currency,
                'status': account.status,
                'balance': float(balance),
                'balance_decimal': str(balance),
                'created_at': account.created_at.isoformat() if account.created_at else None,
                'updated_at': account.updated_at.isoformat() if account.updated_at else None
            }
        except Exception as e:
            logger.error(f"Error getting account with balance {account_id}: {e}")
            return None
    
    @staticmethod
    def get_user_accounts(db: Session, user_id: str) -> List[Dict[str, Any]]:
        """Get all accounts for a user with balances"""
        try:
            accounts = db.query(Account).filter(Account.user_id == user_id).all()
            
            result = []
            for account in accounts:
                balance = LedgerService.calculate_balance(db, account.id)
                
                result.append({
                    'id': str(account.id),
                    'user_id': account.user_id,
                    'account_type': account.account_type,
                    'currency': account.currency,
                    'status': account.status,
                    'balance': float(balance),
                    'balance_decimal': str(balance),
                    'created_at': account.created_at.isoformat() if account.created_at else None,
                    'updated_at': account.updated_at.isoformat() if account.updated_at else None
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting user accounts for {user_id}: {e}")
            return []
    
    @staticmethod
    def update_account_status(
        db: Session,
        account_id: str,
        status: str
    ) -> Optional[Account]:
        """Update account status"""
        try:
            valid_statuses = ['active', 'frozen', 'closed']
            if status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            
            account = AccountService.get_account(db, account_id)
            
            if not account:
                return None
            
            account.status = status
            db.commit()
            
            logger.info(f"Updated account {account_id} status to {status}")
            
            return account
        except Exception as e:
            logger.error(f"Error updating account status for {account_id}: {e}")
            return None
    
    @staticmethod
    def validate_account_currency(db: Session, account_id: str, currency: str) -> bool:
        """Validate that account currency matches expected currency"""
        try:
            account = AccountService.get_account(db, account_id)
            if not account:
                return False
            return account.currency == currency.upper()
        except Exception as e:
            logger.error(f"Error validating account currency: {e}")
            return False
