from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
import uuid

from database import get_db
from services.account_service import AccountService
from services.ledger_service import LedgerService

router = APIRouter(prefix="/accounts", tags=["accounts"])


# Pydantic models
class AccountCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=255, example="user_123")
    account_type: str = Field(..., pattern="^(checking|savings|business)$", example="checking")
    currency: str = Field(default="USD", pattern="^[A-Z]{3}$", example="USD")


class AccountResponse(BaseModel):
    id: str
    user_id: str
    account_type: str
    currency: str
    status: str
    balance: float
    balance_decimal: str
    created_at: str
    updated_at: str | None
    
    class Config:
        from_attributes = True


class LedgerEntryResponse(BaseModel):
    id: str
    account_id: str
    transaction_id: str
    entry_type: str
    amount: float
    created_at: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db)
):
    """Create a new account"""
    try:
        account = AccountService.create_account(
            db=db,
            user_id=account_data.user_id,
            account_type=account_data.account_type,
            currency=account_data.currency
        )
        
        return AccountService.get_account_with_balance(db, account.id)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create account: {str(e)}"
        )


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: str,
    db: Session = Depends(get_db)
):
    """Get account details with balance"""
    try:
        # Validate UUID
        uuid.UUID(account_id)
        
        account_data = AccountService.get_account_with_balance(db, account_id)
        
        if not account_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        return account_data
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve account: {str(e)}"
        )


@router.get("/{account_id}/ledger", response_model=List[LedgerEntryResponse])
def get_account_ledger(
    account_id: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get ledger entries for an account"""
    try:
        # Validate UUID
        uuid.UUID(account_id)
        
        # Check if account exists
        account = AccountService.get_account(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        ledger_entries = LedgerService.get_account_ledger(
            db=db,
            account_id=account_id,
            limit=limit,
            offset=offset
        )
        
        return [
            LedgerEntryResponse(
                id=str(entry.id),
                account_id=str(entry.account_id),
                transaction_id=str(entry.transaction_id),
                entry_type=entry.entry_type,
                amount=float(entry.amount),
                created_at=entry.created_at.isoformat() if entry.created_at else None
            )
            for entry in ledger_entries
        ]
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve ledger: {str(e)}"
        )


@router.get("/user/{user_id}/accounts", response_model=List[AccountResponse])
def get_user_accounts(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all accounts for a user"""
    try:
        accounts = AccountService.get_user_accounts(db, user_id)
        return accounts
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user accounts: {str(e)}"
        )
