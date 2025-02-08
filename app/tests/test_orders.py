from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order():
    response = client.post("/order", json=[{"name": "Corona", "quantity": 2}])
    assert response.status_code == 200
    assert "id" in response.json()
