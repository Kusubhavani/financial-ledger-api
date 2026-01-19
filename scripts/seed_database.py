#!/usr/bin/env python3
"""
Database seeding script for testing and development
"""
import os
import sys
from pathlib import Path
from decimal import Decimal
import random

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from database import SessionLocal
from models.account import Account
from models.transaction import Transaction
from models.ledger_entry import LedgerEntry
from services.account_service import AccountService
from services.transaction_service import TransactionService

def seed_database():
    """Seed the database with test data"""
    db = SessionLocal()
    
    try:
        print("Seeding database...")
        
        # Create test users and accounts
        users = [
            {"id": "user_001", "name": "John Doe"},
            {"id": "user_002", "name": "Jane Smith"},
            {"id": "user_003", "name": "Bob Johnson"},
            {"id": "user_004", "name": "Alice Williams"},
            {"id": "user_005", "name": "Charlie Brown"},
        ]
        
        accounts = []
        
        for user in users:
            # Create checking account
            checking_account = Account(
                user_id=user["id"],
                account_type="checking",
                currency="USD",
                status="active"
            )
            db.add(checking_account)
            accounts.append(checking_account)
            
            # Create savings account
            savings_account = Account(
                user_id=user["id"],
                account_type="savings",
                currency="USD",
                status="active"
            )
            db.add(savings_account)
            accounts.append(savings_account)
        
        db.commit()
        print(f"Created {len(accounts)} accounts for {len(users)} users")
        
        # Create initial deposits
        for account in accounts:
            if account.account_type == "checking":
                amount = Decimal(str(random.randint(1000, 10000)))
            else:
                amount = Decimal(str(random.randint(5000, 50000)))
            
            transaction = Transaction(
                type="deposit",
                status="completed",
                amount=amount,
                currency="USD",
                description=f"Initial deposit for {account.account_type} account"
            )
            db.add(transaction)
            db.flush()
            
            ledger_entry = LedgerEntry(
                account_id=account.id,
                transaction_id=transaction.id,
                entry_type="credit",
                amount=amount
            )
            db.add(ledger_entry)
        
        db.commit()
        print("Created initial deposits")
        
        # Create some transfers between accounts
        checking_accounts = [acc for acc in accounts if acc.account_type == "checking"]
        savings_accounts = [acc for acc in accounts if acc.account_type == "savings"]
        
        for i in range(10):
            source = random.choice(checking_accounts)
            destination = random.choice(savings_accounts)
            
            # Ensure source and destination are different
            if source.user_id == destination.user_id:
                continue
            
            amount = Decimal(str(random.randint(100, 1000)))
            
            try:
                transaction = TransactionService.execute_transfer(
                    db=db,
                    source_account_id=source.id,
                    destination_account_id=destination.id,
                    amount=amount,
                    currency="USD",
                    description=f"Transfer {i+1}"
                )
                print(f"Created transfer: {amount} USD from {source.user_id} to {destination.user_id}")
            except Exception as e:
                print(f"Failed to create transfer: {e}")
                continue
        
        # Create some withdrawals
        for account in random.sample(checking_accounts, 3):
            amount = Decimal(str(random.randint(50, 500)))
            
            transaction = TransactionService.execute_withdrawal(
                db=db,
                account_id=account.id,
                amount=amount,
                currency="USD",
                description="ATM withdrawal"
            )
            print(f"Created withdrawal: {amount} USD from {account.user_id}")
        
        db.commit()
        print("\nDatabase seeding completed successfully!")
        
        # Print summary
        print("\n=== SEEDING SUMMARY ===")
        print(f"Total users: {len(users)}")
        print(f"Total accounts: {len(accounts)}")
        
        total_transactions = db.query(Transaction).count()
        total_ledger_entries = db.query(LedgerEntry).count()
        
        print(f"Total transactions: {total_transactions}")
        print(f"Total ledger entries: {total_ledger_entries}")
        
        # Show sample account balances
        print("\n=== SAMPLE ACCOUNT BALANCES ===")
        for account in random.sample(accounts, 5):
            from services.ledger_service import LedgerService
            balance = LedgerService.calculate_balance(db, account.id)
            print(f"{account.user_id} - {account.account_type}: ${balance}")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
