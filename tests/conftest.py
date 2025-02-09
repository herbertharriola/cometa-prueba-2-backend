import pytest
from app.services.order_service import orders, beers_data

@pytest.fixture(autouse=True)
def reset_data():
    """Reinicia las órdenes y el stock de cervezas antes de cada prueba."""
    orders.clear()
    beers_data["beers"] = [
        {"name": "Corona", "price": 115, "quantity": 10},
        {"name": "Quilmes", "price": 120, "quantity": 10},
        {"name": "Club Colombia", "price": 110, "quantity": 10},
        {"name": "Gallo", "price": 130, "quantity": 10},
    ]