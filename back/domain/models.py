from dataclasses import dataclass
from datetime import datetime
from typing import Literal

PrintResult = Literal["APPROVED", "REJECTED"]
EventType = Literal["PRINT", "REPRINT", "REJECTED"]


@dataclass(frozen=True)
class Product:
    product_code: str
    product_description: str
    requested_qty: int
    uom: str


@dataclass(frozen=True)
class Document:
    document_type: str
    document_number: str
    status: str


@dataclass(frozen=True)
class Label:
    etq_id: str
    lpn_id: str
    is_pre_generated: bool
    template_code: str
    zpl: str


@dataclass(frozen=True)
class Order:
    request_id: str
    request_datetime: str
    requested_by: str
    zone: str
    document: Document
    labels: list[Label]
    products: list[Product]
    reprint_reason: str | None = None

    def primary_label(self) -> Label:
        return self.labels[0]


@dataclass(frozen=True)
class InventoryItem:
    zone: str
    product_code: str
    available_qty: int
    is_supplied: bool


@dataclass(frozen=True)
class PrintDecision:
    result: PrintResult
    reasons: list[str]

    @property
    def is_approved(self) -> bool:
        return self.result == "APPROVED"


@dataclass(frozen=True)
class AuditEvent:
    request_id: str
    timestamp: datetime
    requested_by: str
    zone: str
    etq_id: str
    lpn_id: str
    result: PrintResult
    event_type: EventType
    reasons: list[str]
    reprint_reason: str | None = None
