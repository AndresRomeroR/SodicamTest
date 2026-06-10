from domain.models import InventoryItem, Order, PrintDecision

BLOCKED_DOCUMENT_STATUSES = {"ANULADA", "DEVUELTA"}


def evaluate_print(order: Order | None, inventory: dict[str, InventoryItem]) -> PrintDecision:
    if order is None:
        return PrintDecision(result="REJECTED", reasons=["La ETQ/LPN no existe en los datos mock"])

    reasons: list[str] = []

    if not order.labels:
        reasons.append("La orden no tiene ETQ/LPN pre-generada")
    elif not order.primary_label().is_pre_generated:
        reasons.append("La etiqueta no esta marcada como pre-generada")

    document_status = order.document.status.upper()
    if document_status in BLOCKED_DOCUMENT_STATUSES:
        reasons.append(f"Documento origen en estado invalido: {document_status}")

    for product in order.products:
        inventory_item = inventory.get(product.product_code)
        if inventory_item is None:
            reasons.append(f"Producto {product.product_code} sin inventario para la zona {order.zone}")
            continue
        if not inventory_item.is_supplied:
            reasons.append(f"Producto {product.product_code} no abastecido para la zona {order.zone}")
        if inventory_item.available_qty < product.requested_qty:
            reasons.append(
                f"Producto {product.product_code} con disponibilidad insuficiente: "
                f"requiere {product.requested_qty}, disponible {inventory_item.available_qty}"
            )

    if reasons:
        return PrintDecision(result="REJECTED", reasons=reasons)

    return PrintDecision(result="APPROVED", reasons=[])
