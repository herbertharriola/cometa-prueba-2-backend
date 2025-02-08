from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class OrderItem(BaseModel):
    name: str
    price_per_unit: float
    quantity: int
    total: float = Field(default=0)
    ordered_by: str  # Indica quién pidió la cerveza

    @classmethod
    def calculate_total(cls, price_per_unit: float, quantity: int) -> float:
        return round(price_per_unit * quantity, 2)

    def __init__(self, **data):
        super().__init__(**data)
        self.total = self.calculate_total(self.price_per_unit, self.quantity)

class Order(BaseModel):
    id: int
    created: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    paid: bool = False
    subtotal: float = 0
    taxes: float = 0
    total: float = 0
    items: List[OrderItem] = []
    payments: Dict[str, float] = {"Amigo 1": 0, "Amigo 2": 0, "Amigo 3": 0}  # Registro de pagos

class OrderRequestCreate(BaseModel):
    items: List[dict]
    ordered_by: str

class OrderRequestUpdate(BaseModel):
    order_id: int
    items: List[dict]
    ordered_by: str

class PayOrderRequest(BaseModel):
    order_id: int
    amount: float
    friend: str