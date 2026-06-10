import json
from pathlib import Path

from domain.models import Document, InventoryItem, Label, Order, Product


class MockRepository:
    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or Path(__file__).resolve().parent / "mocks"

    def find_order(self, identifier: str) -> Order | None:
        normalized = identifier.strip().lower()
        for order in self._load_orders():
            labels = order.labels
            if any(label.lpn_id.lower() == normalized or label.etq_id.lower() == normalized for label in labels):
                return order
        return None

    def get_inventory_by_zone(self, zone: str) -> dict[str, InventoryItem]:
        normalized_zone = zone.strip().upper()
        inventory_items = self._read_json("inventory.json")
        result: dict[str, InventoryItem] = {}
        for item in inventory_items:
            if item["zone"].upper() != normalized_zone:
                continue
            inventory_item = InventoryItem(
                zone=item["zone"],
                product_code=item["productCode"],
                available_qty=item["availableQty"],
                is_supplied=item["isSupplied"],
            )
            result[inventory_item.product_code] = inventory_item
        return result

    def _load_orders(self) -> list[Order]:
        return [self._map_order(item) for item in self._read_json("orders.json")]

    def _read_json(self, file_name: str):
        with (self.base_path / file_name).open(encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _map_order(item: dict) -> Order:
        document = Document(
            document_type=item["document"]["documentType"],
            document_number=item["document"]["documentNumber"],
            status=item["document"]["status"],
        )
        labels = [
            Label(
                etq_id=label["etqId"],
                lpn_id=label["lpnId"],
                is_pre_generated=label["isPreGenerated"],
                template_code=label["templateCode"],
                zpl=label["zpl"],
            )
            for label in item["labels"]
        ]
        products = [
            Product(
                product_code=product["productCode"],
                product_description=product["productDescription"],
                requested_qty=product["requestedQty"],
                uom=product["uom"],
            )
            for product in item["products"]
        ]
        return Order(
            request_id=item["requestId"],
            request_datetime=item["requestDateTime"],
            requested_by=item["requestedBy"],
            zone=item["zone"],
            document=document,
            labels=labels,
            products=products,
            reprint_reason=item.get("reprintReason"),
        )
