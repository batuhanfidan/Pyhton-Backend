from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_ledger_entry():
    response = client.post("/ledger", json={
        "operation": "CREDIT_ADD",
        "amount": 10,
        "owner_id": "user123",
        "nonce": "unique_nonce_123"
    })
    assert response.status_code == 200

def test_get_ledger_balance():
    response = client.get("/ledger/user123")
    assert response.status_code == 200
    assert "balance" in response.json()
