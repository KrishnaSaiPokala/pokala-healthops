from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_health_and_incident_flow():
    assert client.get("/health").json()["no_phi"] is True
    client.post("/incident-demo")
    client.post("/replay/INC-20260602-LAB-CODE-FORMAT")
    assert client.get("/summary").json()["dlq_open"] == 0
    assert client.get("/metrics").status_code == 200
