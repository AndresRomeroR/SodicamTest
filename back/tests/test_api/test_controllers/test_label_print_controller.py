from pathlib import Path

from fastapi.testclient import TestClient

from api.main import create_app


def test_print_label_accepts_legacy_request(tmp_path, monkeypatch):
    monkeypatch.setenv("ETQ_HISTORY_FILE", str(tmp_path / "history.json"))
    client = TestClient(create_app())

    response = client.post("/api/v1/labels/print", json={"request": {"lpn": "olpn12345"}})

    assert response.status_code == 200
    body = response.json()
    assert body["isSuccessful"] is True
    assert body["result"]["result"] == "APPROVED"


def test_history_endpoint_returns_audit_events(tmp_path, monkeypatch):
    monkeypatch.setenv("ETQ_HISTORY_FILE", str(tmp_path / "history.json"))
    client = TestClient(create_app())

    client.post("/api/v1/labels/print", json={"lpn": "olpn-annulled"})
    response = client.get("/api/v1/labels/history?identifier=olpn-annulled")

    assert response.status_code == 200
    assert response.json()["result"][0]["result"] == "REJECTED"
