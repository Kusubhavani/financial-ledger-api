import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from database import Base, get_db
from config import settings

# Test database
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Create test client with overridden database dependency"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_account_data():
    return {
        "user_id": "user_123",
        "account_type": "checking",
        "currency": "USD"
    }

@pytest.fixture
def sample_transfer_data():
    return {
        "source_account_id": "",
        "destination_account_id": "",
        "amount": 100.50,
        "currency": "USD",
        "description": "Test transfer"
    }

@pytest.fixture
def sample_deposit_data():
    return {
        "account_id": "",
        "amount": 500.00,
        "currency": "USD",
        "description": "Test deposit"
    }

@pytest.fixture
def sample_withdrawal_data():
    return {
        "account_id": "",
        "amount": 50.00,
        "currency": "USD",
        "description": "Test withdrawal"
    }
