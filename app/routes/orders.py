from fastapi import APIRouter
from app.models.order import OrderRequestCreate, OrderRequestUpdate
from app.services.order_service import create_order, get_orders, get_order, update_order

router = APIRouter()

@router.get("/orders")
def list_orders():
    return get_orders()

@router.get("/order/{order_id}")
def order_status(order_id: int):
    return get_order(order_id)

@router.post("/order")
def new_order(order_request: OrderRequestCreate):
    return create_order(order_request)

@router.put("/order")
def modify_order(order_request: OrderRequestUpdate):
    return update_order(order_request)