import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests import test_orders

client = TestClient(app)

def test_pay_order():
    """Prueba realizar un pago correctamente."""
    test_orders.test_create_order()
    payment_data = {
        "order_id": 1,
        "amount": 50,
        "friend": "Amigo 1"
    }
    response = client.post("/pay", json=payment_data)
    assert response.status_code == 200, response.text
    assert "Pago recibido" in response.json()["message"]

def test_payment_exceeds_balance():
    """Prueba que no se pueda pagar más de lo debido."""
    test_orders.test_create_order()
    payment_data = {
        "order_id": 1,
        "amount": 1000,  # Más de lo permitido
        "friend": "Amigo 2"
    }
    response = client.post("/pay", json=payment_data)
    assert response.status_code == 400
    assert "El monto supera el saldo pendiente de la orden" in response.json()["detail"]

def test_payment_duplicate():
    """Prueba que un amigo no pueda pagar dos veces."""
    test_orders.test_create_order()
    payment_data = {
        "order_id": 1,
        "amount": 50,
        "friend": "Amigo 1"
    }
    response = client.post("/pay", json=payment_data)
    assert response.status_code == 200

    # Intentar pagar nuevamente con el mismo amigo
    response = client.post("/pay", json=payment_data)
    assert response.status_code == 400
    assert "Este amigo ya ha realizado un pago" in response.json()["detail"]

def test_split_bill():
    """Prueba la división de la cuenta en partes iguales."""
    test_orders.test_create_order()
    response = client.get("/payment/1?method=split")
    assert response.status_code == 200
    json_response = response.json()
    assert "each_pays" in json_response
    assert len(json_response["each_pays"]) == 3

def test_individual_bill():
    """Prueba la división de la cuenta por consumo individual."""
    test_orders.test_create_order()
    response = client.get("/payment/1?method=individual")
    assert response.status_code == 200
    json_response = response.json()
    assert "individual_totals" in json_response
    assert "Amigo 1" in json_response["individual_totals"]
