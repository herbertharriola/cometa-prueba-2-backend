from fastapi import HTTPException
from app.models.order import Order
from app.data import orders

def split_bill(order_id: int, method: str):
    order = next((o for o in orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    if method == "split":
        base_amount = round(order.subtotal / 3, 2)
        base_tax = round(order.taxes / 3, 2)
        total_split = base_amount * 3 + base_tax * 3
        difference = round(order.total - total_split, 2)

        payments = [{"amount": base_amount + base_tax} for _ in range(3)]
        if difference != 0:
            payments[0]["amount"] += difference  # Ajustar el primer amigo con el centavo faltante

        return {"each_pays": payments}

    elif method == "individual":
        individual_totals = {}

        for item in order.items:
            if item.ordered_by not in individual_totals:
                individual_totals[item.ordered_by] = 0
            individual_totals[item.ordered_by] += round(item.total, 2)

        # Calcular impuestos proporcionalmente a cada usuario
        total_subtotal = order.subtotal
        for friend in individual_totals:
            percentage = individual_totals[friend] / total_subtotal
            tax_share = round(order.taxes * percentage, 2)
            individual_totals[friend] += tax_share

        return {"individual_totals": individual_totals}