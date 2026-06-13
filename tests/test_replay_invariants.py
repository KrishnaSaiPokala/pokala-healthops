from sqlalchemy import select

from openhip.db import SessionLocal
from openhip.models import DeadLetterMessage, Observation
from openhip.pipeline import INCIDENT_ID, incident_demo, replay_incident, verify_warehouse
from openhip.reliability import assert_replay_invariants, replay_invariant_snapshot


def test_replay_closes_dlq_and_preserves_recovery_invariants():
    incident_demo(total=40, bad_count=10)
    replay_incident(INCIDENT_ID)
    verify_warehouse()

    snapshot = assert_replay_invariants(INCIDENT_ID)

    assert snapshot["incident_status"] == "remediated"
    assert snapshot["open_dlq"] == 0
    assert snapshot["replayed_failed_dlq"] == 0
    assert "incident_opened" in snapshot["audit_actions"]
    assert "replay_completed" in snapshot["audit_actions"]


def test_replay_is_idempotent_after_incident_is_remediated():
    incident_demo(total=40, bad_count=10)
    replay_incident(INCIDENT_ID)
    verify_warehouse()

    before = replay_invariant_snapshot(INCIDENT_ID)
    replay_incident(INCIDENT_ID)
    verify_warehouse()
    after = replay_invariant_snapshot(INCIDENT_ID)

    assert after["open_dlq"] == 0
    assert after["observations"] == before["observations"]
    assert after["replayed_accepted_dlq"] == before["replayed_accepted_dlq"]


def test_replay_marks_each_dlq_record_once():
    incident_demo(total=40, bad_count=10)
    replay_incident(INCIDENT_ID)

    with SessionLocal() as db:
        dlq_records = list(
            db.scalars(
                select(DeadLetterMessage).where(DeadLetterMessage.incident_id == INCIDENT_ID)
            )
        )
        observations = list(db.scalars(select(Observation)))

    assert len(dlq_records) == 10
    assert all(record.replay_count == 1 for record in dlq_records)
    assert all(record.status == "replayed_accepted" for record in dlq_records)
    assert len(observations) == 40
