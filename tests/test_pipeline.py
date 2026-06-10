from openhip.pipeline import incident_demo, replay_incident, verify_warehouse


def test_incident_replay_recovery():
    initial = incident_demo(total=20, bad_count=5)
    assert initial["dlq_open"] == 5

    after = replay_incident()
    assert after["dlq_open"] == 0

    quality = verify_warehouse()
    assert quality["failed_checks"] == 0
