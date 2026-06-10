import os
import json
from datetime import datetime
from pathlib import Path

from domain.models import AuditEvent


class AuditRepository:
    def __init__(self, history_file: Path | None = None, seed_file: Path | None = None):
        default_history = Path(__file__).resolve().parents[1] / "data" / "print_history.json"
        self.history_file = history_file or Path(os.getenv("ETQ_HISTORY_FILE", default_history))
        self.seed_file = seed_file or Path(__file__).resolve().parent / "mocks" / "print_history.json"

    def list_events(self, identifier: str | None = None) -> list[dict]:
        events = self._load_events()
        if identifier is None:
            return events
        normalized = identifier.strip().lower()
        return [
            event
            for event in events
            if event["lpnId"].lower() == normalized or event["etqId"].lower() == normalized
        ]

    def has_successful_print(self, lpn_id: str, etq_id: str) -> bool:
        for event in self.list_events():
            same_label = event["lpnId"].lower() == lpn_id.lower() or event["etqId"].lower() == etq_id.lower()
            if same_label and event["result"] == "APPROVED":
                return True
        return False

    def save(self, event: AuditEvent) -> dict:
        events = self._load_events()
        serialized = {
            "requestId": event.request_id,
            "timestamp": event.timestamp.isoformat(),
            "requestedBy": event.requested_by,
            "zone": event.zone,
            "etqId": event.etq_id,
            "lpnId": event.lpn_id,
            "result": event.result,
            "eventType": event.event_type,
            "reasons": event.reasons,
            "reprintReason": event.reprint_reason,
        }
        events.append(serialized)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with self.history_file.open("w", encoding="utf-8") as file:
            json.dump(events, file, ensure_ascii=False, indent=2)
        return serialized

    def _load_events(self) -> list[dict]:
        source = self.history_file if self.history_file.exists() else self.seed_file
        if not source.exists():
            return []
        with source.open(encoding="utf-8") as file:
            events = json.load(file)
        return sorted(events, key=lambda event: datetime.fromisoformat(event["timestamp"]), reverse=True)
