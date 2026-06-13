from pathlib import Path

from openhip.pipeline import (
    INCIDENT_ID,
    export_incident_report,
    incident_demo,
    replay_incident,
    verify_warehouse,
)
from openhip.reliability import validate_incident_report, write_replay_invariant_report


def test_exported_incident_report_has_required_proof_fields():
    incident_demo(total=40, bad_count=10)
    replay_incident(INCIDENT_ID)
    verify_warehouse()
    path = export_incident_report(INCIDENT_ID)

    report = validate_incident_report(path)

    assert report["incident_id"] == INCIDENT_ID
    assert report["dlq"]["open"] == 0
    assert report["warehouse"]["quality"]["failed_checks"] == 0


def test_replay_invariant_report_is_written_to_evidence_folder():
    incident_demo(total=40, bad_count=10)
    replay_incident(INCIDENT_ID)
    verify_warehouse()

    path = write_replay_invariant_report(INCIDENT_ID)

    assert path == Path("evidence/replay-invariants.json")
    assert path.exists()
