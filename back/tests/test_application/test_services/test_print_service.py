from pathlib import Path

from application.services.print_service import PrintService
from infrastructure.audit_repository import AuditRepository
from infrastructure.mock_repository import MockRepository


def build_service(tmp_path: Path) -> PrintService:
    mocks_path = Path(__file__).resolve().parents[3] / "infrastructure" / "mocks"
    return PrintService(
        mock_repository=MockRepository(mocks_path),
        audit_repository=AuditRepository(history_file=tmp_path / "history.json", seed_file=mocks_path / "print_history.json"),
    )


def test_process_successful_print(tmp_path):
    result = build_service(tmp_path).process("olpn12345")

    assert result["result"] == "APPROVED"
    assert result["eventType"] == "PRINT"
    assert result["label"]["zpl"]


def test_process_reprint_when_previous_success_exists(tmp_path):
    result = build_service(tmp_path).process("olpn-reprint", reprint_reason="Etiqueta ilegible")

    assert result["result"] == "APPROVED"
    assert result["isReprint"] is True
    assert result["eventType"] == "REPRINT"
    assert result["reprintReason"] == "Etiqueta ilegible"


def test_process_rejection_is_audited(tmp_path):
    service = build_service(tmp_path)
    result = service.process("olpn-shortage")
    history = service.history("olpn-shortage")

    assert result["result"] == "REJECTED"
    assert history[0]["eventType"] == "REJECTED"
    assert history[0]["reasons"]
