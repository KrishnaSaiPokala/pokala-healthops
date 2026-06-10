from openhip.pipeline import incident_demo, replay_incident, verify_warehouse


def test_incident_detects_and_recovers():
    initial = incident_demo(total=40, bad_count=10)
    assert initial["dlq_open"] == 10

    after = replay_incident()
    assert after["dlq_open"] == 0

    quality = verify_warehouse()
    assert quality["failed_checks"] == 0
    assert quality["passed_checks"] == 3
