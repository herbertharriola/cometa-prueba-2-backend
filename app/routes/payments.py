from fastapi import APIRouter
from app.services.payment_service import split_bill
from app.services.order_service import pay_order
from app.models.order import PayOrderRequest

router = APIRouter()

@router.get("/payment/{order_id}")
def get_payment(order_id: int, method: str):
    return split_bill(order_id, method)

@router.post("/pay")
def make_payment(pay_order_request: PayOrderRequest):
    return pay_order(pay_order_request)
