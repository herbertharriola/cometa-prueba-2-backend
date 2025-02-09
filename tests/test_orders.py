import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_orders():
    """Prueba que la lista de órdenes se obtenga correctamente."""
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_order():
    """Prueba la creación de una nueva orden."""
    order_data = {
        "items": [
            {"name": "Corona", "quantity": 2}
        ],
        "ordered_by": "Amigo 1"
    }
    response = client.post("/order", json=order_data)
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert "id" in json_response
    assert json_response["subtotal"] > 0
    assert len(json_response["items"]) == 1

def test_get_order_status():
    """Prueba la obtención del estado de una orden existente."""
    test_create_order()
    response = client.get("/order/1")
    assert response.status_code == 200
    json_response = response.json()
    assert "subtotal" in json_response
    assert "items" in json_response

def test_update_order():
    """Prueba actualizar una orden existente."""
    test_create_order()
    update_data = {
        "order_id": 1,
        "items": [
            {"name": "Quilmes", "quantity": 1}
        ],
        "ordered_by": "Amigo 2"
    }
    response = client.put("/order", json=update_data)
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert json_response["message"] == "Orden actualizada correctamente"
    assert "order" in json_response

def test_order_insufficient_stock():
    """Prueba crear una orden con cantidad mayor al stock disponible."""
    order_data = {
        "items": [
            {"name": "Corona", "quantity": 20}  # Excediendo stock
        ],
        "ordered_by": "Amigo 1"
    }
    response = client.post("/order", json=order_data)
    assert response.status_code == 400
    assert "No hay suficiente stock de Corona" in response.json()["detail"]
