from app.models.order import Order, OrderItem, OrderRequestCreate, OrderRequestUpdate, PayOrderRequest
from app.data import orders, beers_data
from fastapi import HTTPException
from datetime import datetime

def create_order(order_request: OrderRequestCreate):    
    order_id = len(orders) + 1
    subtotal = 0
    items_with_stock = []

    for item in order_request.items:
        # Buscar la cerveza en el stock
        beer = next((b for b in beers_data["beers"] if b["name"] == item["name"]), None)
        if not beer or beer["quantity"] < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"No hay suficiente stock de {item['name']}")

        # Restar la cantidad del stock
        beer["quantity"] -= item["quantity"]

        # Crear el item con los datos correctos
        order_item = OrderItem(
            name=item["name"], 
            price_per_unit=beer["price"],  # Se obtiene del stock
            quantity=item["quantity"], 
            ordered_by=order_request.ordered_by
        )

        items_with_stock.append(order_item)
        subtotal += order_item.total  # Sumar el total calculado

    # Calcular impuestos y total
    taxes = subtotal * 0.12
    total = subtotal + taxes

    # Crear orden
    order = Order(
        id=order_id,
        created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        subtotal=subtotal,
        taxes=taxes,
        total=total,
        items=items_with_stock
    )

    orders.append(order)
    return order

def get_orders():
    return orders

def get_order(order_id: int):
    if order_id >= len(orders) + 1:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return next((order for order in orders if order.id == order_id), None)

def pay_order(pay_order_request: PayOrderRequest):
    order = next((order for order in orders if order.id == pay_order_request.order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    if pay_order_request.friend not in order.payments:
        raise HTTPException(status_code=400, detail="Amigo no válido")
    
    if order.payments[pay_order_request.friend] > 0:
        raise HTTPException(status_code=400, detail="Este amigo ya ha realizado un pago")
    
    # Suma los payments y valida el balance restante
    total_paid = sum(order.payments.values())
    remaining_balance = order.total - total_paid
    
    if pay_order_request.amount > remaining_balance:
        raise HTTPException(status_code=400, detail="El monto supera el saldo pendiente de la orden")
    
    # Suma lo pagado por el amigo
    order.payments[pay_order_request.friend] += pay_order_request.amount
    total_paid = sum(order.payments.values())
    
    # Valida si pone la orden en estado pagada
    if total_paid >= order.total:
        order.paid = True
    
    return {"message": "Pago recibido", "order": order}

def update_order(order_request: OrderRequestUpdate):
    # Buscar la orden existente
    order = next((order for order in orders if order.id == order_request.order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    for item in order_request.items:
        beer = next((b for b in beers_data["beers"] if b["name"] == item["name"]), None)
        if not beer or beer["quantity"] < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"No hay suficiente stock de {item['name']}")

        # Restar del stock
        beer["quantity"] -= item["quantity"]

        # Si el item ya existe en la orden, solo aumentar la cantidad y total
        existing_item = next((i for i in order.items if i.name == item["name"]), None)
        if existing_item:
            existing_item.quantity += item["quantity"]
            existing_item.total += beer["price"] * item["quantity"]
        else:
            # Agregar el `price_per_unit` antes de crear el nuevo item
            item_with_price = {
                "name": item["name"],
                "quantity": item["quantity"],
                "price_per_unit": beer["price"],  # 🔥 Agregamos el precio aquí
                "ordered_by": order_request.ordered_by
            }
            order.items.append(OrderItem(**item_with_price))

    # Recalcular totales
    order.subtotal = sum(i.quantity * next(b["price"] for b in beers_data["beers"] if b["name"] == i.name) for i in order.items)
    order.taxes = order.subtotal * 0.12
    order.total = order.subtotal + order.taxes

    return {"message": "Orden actualizada correctamente", "order": order}