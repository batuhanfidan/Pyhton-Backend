import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import LedgerOperation

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield db  

    db.close()
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_add_ledger_entry(test_db):
    # Test 1: Başarılı işlem ekleme
    response = client.post("/ledger", json={
        "operation": "CREDIT_ADD",
        "amount": 100,
        "owner_id": "user123",
        "nonce": "unique_nonce_123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction added successfully"
    
    # Test 2: Aynı nonce ile tekrar deneme (hata vermeli)
    response = client.post("/ledger", json={
        "operation": "CREDIT_ADD",
        "amount": 50,
        "owner_id": "user123",
        "nonce": "unique_nonce_123"
    })
    assert response.status_code == 400
    assert "Duplicate transaction" in response.json()["detail"]
    
    # Test 3: Negatif miktar ile işlem
    response = client.post("/ledger", json={
        "operation": "CREDIT_SPEND",
        "amount": -50,
        "owner_id": "user123",
        "nonce": "unique_nonce_456"
    })
    assert response.status_code == 200

def test_get_ledger_balance(test_db):
    # Test verisi oluştur
    client.post("/ledger", json={
        "operation": "CREDIT_ADD",
        "amount": 100,
        "owner_id": "test_user",
        "nonce": "balance_test_1"
    })
    
    client.post("/ledger", json={
        "operation": "CREDIT_SPEND",
        "amount": -30,
        "owner_id": "test_user",
        "nonce": "balance_test_2"
    })
    
    # Bakiye kontrolü
    response = client.get("/ledger/test_user")
    assert response.status_code == 200
    assert "balance" in response.json()
    assert response.json()["balance"] == 70  # 100 - 30
    
    # Olmayan kullanıcı için bakiye kontrolü
    response = client.get("/ledger/nonexistent_user")
    assert response.status_code == 200
    assert response.json()["balance"] == 0

def test_different_operations(test_db):
    # Farklı işlem türlerini test et
    operations = [
        ("SIGNUP_CREDIT", 500),
        ("DAILY_REWARD", 100),
        ("CONTENT_CREATION", 50),
        ("CONTENT_ACCESS", -10)
    ]
    
    user_id = "operation_test_user"
    expected_balance = 0
    
    for op_type, amount in operations:
        response = client.post("/ledger", json={
            "operation": op_type,
            "amount": amount,
            "owner_id": user_id,
            "nonce": f"test_op_{op_type}"
        })
        assert response.status_code == 200
        expected_balance += amount
    
    # Toplam bakiye kontrolü
    response = client.get(f"/ledger/{user_id}")
    assert response.status_code == 200
    assert response.json()["balance"] == expected_balance

def test_invalid_requests(test_db):
    # Geçersiz operation type
    response = client.post("/ledger", json={
        "operation": "INVALID_OP",
        "amount": 100,
        "owner_id": "user123",
        "nonce": "invalid_op_test"
    })
    assert response.status_code == 422  # Validation Error
    
    # Eksik alan
    response = client.post("/ledger", json={
        "amount": 100,
        "owner_id": "user123"
    })
    assert response.status_code == 422
