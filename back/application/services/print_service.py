from datetime import datetime, timezone
from uuid import uuid4

from domain.models import AuditEvent, Order
from domain.print_rules import evaluate_print
from infrastructure.audit_repository import AuditRepository
from infrastructure.mock_repository import MockRepository


class PrintService:
    def __init__(
        self,
        mock_repository: MockRepository | None = None,
        audit_repository: AuditRepository | None = None,
    ):
        self.mock_repository = mock_repository or MockRepository()
        self.audit_repository = audit_repository or AuditRepository()

    def process(
        self,
        identifier: str,
        zone: str | None = None,
        requested_by: str | None = None,
        reprint_reason: str | None = None,
    ) -> dict:
        order = self.mock_repository.find_order(identifier)
        if order and zone:
            order = Order(
                request_id=order.request_id,
                request_datetime=order.request_datetime,
                requested_by=order.requested_by,
                zone=zone,
                document=order.document,
                labels=order.labels,
                products=order.products,
                reprint_reason=order.reprint_reason,
            )

        inventory = self.mock_repository.get_inventory_by_zone(order.zone) if order else {}
        decision = evaluate_print(order, inventory)
        label = order.primary_label() if order else None

        is_reprint = False
        if decision.is_approved and label:
            is_reprint = self.audit_repository.has_successful_print(label.lpn_id, label.etq_id)

        event = AuditEvent(
            request_id=f"AUD-{uuid4().hex[:12].upper()}",
            timestamp=datetime.now(timezone.utc),
            requested_by=requested_by or (order.requested_by if order else "unknown"),
            zone=order.zone if order else (zone or "unknown"),
            etq_id=label.etq_id if label else identifier,
            lpn_id=label.lpn_id if label else identifier,
            result=decision.result,
            event_type="REPRINT" if is_reprint else ("PRINT" if decision.is_approved else "REJECTED"),
            reasons=decision.reasons,
            reprint_reason=reprint_reason or (order.reprint_reason if order else None),
        )
        persisted_event = self.audit_repository.save(event)

        return self._build_response(order, decision.reasons, persisted_event, is_reprint)

    def history(self, identifier: str | None = None) -> list[dict]:
        return self.audit_repository.list_events(identifier)

    @staticmethod
    def _build_response(order: Order | None, reasons: list[str], event: dict, is_reprint: bool) -> dict:
        if order is None:
            return {
                "requestId": event["requestId"],
                "result": event["result"],
                "eventType": event["eventType"],
                "isReprint": False,
                "rejectionReasons": reasons,
            }

        label = order.primary_label()
        return {
            "requestId": event["requestId"],
            "result": event["result"],
            "eventType": event["eventType"],
            "isReprint": is_reprint,
            "requestedBy": event["requestedBy"],
            "zone": event["zone"],
            "document": {
                "documentType": order.document.document_type,
                "documentNumber": order.document.document_number,
                "status": order.document.status,
            },
            "label": {
                "etqId": label.etq_id,
                "lpnId": label.lpn_id,
                "templateCode": label.template_code,
                "zpl": label.zpl if event["result"] == "APPROVED" else None,
            },
            "products": [
                {
                    "productCode": product.product_code,
                    "productDescription": product.product_description,
                    "requestedQty": product.requested_qty,
                    "uom": product.uom,
                }
                for product in order.products
            ],
            "rejectionReasons": reasons,
            "reprintReason": event["reprintReason"],
        }
