from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_payment():
    client.post("/order", json=[{"name": "Corona", "quantity": 2}])
    response = client.post("/payment/0", params={"amount": 300})
    assert response.status_code == 200
    assert response.json()["message"] == "Pago recibido"
