from domain.models import Document, InventoryItem, Label, Order, Product
from domain.print_rules import evaluate_print


def build_order(status: str = "LIBERADA") -> Order:
    return Order(
        request_id="REQ-1",
        request_datetime="2026-06-05T10:15:00-05:00",
        requested_by="tester",
        zone="ZONA-PICKING-A",
        document=Document(document_type="NOTA_PEDIDO", document_number="NP-1", status=status),
        labels=[
            Label(
                etq_id="ETQ-1",
                lpn_id="LPN-1",
                is_pre_generated=True,
                template_code="TPL",
                zpl="^XA^XZ",
            )
        ],
        products=[Product(product_code="PROD-1", product_description="Item", requested_qty=2, uom="UND")],
    )


def test_rejects_missing_lpn():
    decision = evaluate_print(None, {})

    assert decision.result == "REJECTED"
    assert "no existe" in decision.reasons[0]


def test_rejects_blocked_document_status():
    decision = evaluate_print(
        build_order(status="ANULADA"),
        {"PROD-1": InventoryItem(zone="ZONA-PICKING-A", product_code="PROD-1", available_qty=5, is_supplied=True)},
    )

    assert decision.result == "REJECTED"
    assert "ANULADA" in decision.reasons[0]


def test_rejects_insufficient_inventory():
    decision = evaluate_print(
        build_order(),
        {"PROD-1": InventoryItem(zone="ZONA-PICKING-A", product_code="PROD-1", available_qty=1, is_supplied=True)},
    )

    assert decision.result == "REJECTED"
    assert "disponibilidad insuficiente" in decision.reasons[0]


def test_approves_valid_print():
    decision = evaluate_print(
        build_order(),
        {"PROD-1": InventoryItem(zone="ZONA-PICKING-A", product_code="PROD-1", available_qty=2, is_supplied=True)},
    )

    assert decision.result == "APPROVED"
    assert decision.reasons == []
