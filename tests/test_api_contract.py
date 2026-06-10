from fastapi.testclient import TestClient

from apps.api.main import app
from openhip.pipeline import incident_demo, replay_incident, verify_warehouse


def test_api_contract_after_replay_recovery():
    incident_demo(total=20, bad_count=5)
    replay_incident()
    verify_warehouse()

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/health").json()["no_phi"] is True
    assert client.get("/summary").json()["dlq_open"] == 0
    assert client.get("/incidents").json()[0]["status"] == "remediated"
    assert all(row["status"] == "passed" for row in client.get("/quality").json())
