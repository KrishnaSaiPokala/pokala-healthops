from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from sqlalchemy import func, select

from openhip.db import SessionLocal, init_db
from openhip.models import (
    AuditEvent,
    DeadLetterMessage,
    Incident,
    IntegrationRun,
    Observation,
    QualityCheck,
)

REQUIRED_REPORT_KEYS = {
    "incident_id",
    "status",
    "primary_failure",
    "failed_rule",
    "failed_messages",
    "run",
    "dlq",
    "warehouse",
    "no_phi",
    "generated_at",
}

REQUIRED_AUDIT_ACTIONS = {"incident_opened", "replay_completed"}


def replay_invariant_snapshot(incident_id: str) -> dict[str, Any]:
    """Return the recovery invariants that matter for this repository.

    This is intentionally separate from the demo commands. Staff-level proof
    should be queryable without reading console output.
    """
    init_db()
    with SessionLocal() as db:
        incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
        run = db.scalar(select(IntegrationRun).where(IntegrationRun.incident_id == incident_id))

        source_ids = list(db.scalars(select(Observation.source_message_id)))
        duplicate_sources = sorted(
            source_id for source_id, count in Counter(source_ids).items() if count > 1
        )

        actions = set(
            db.scalars(
                select(AuditEvent.action).where(AuditEvent.resource_id == incident_id)
            )
        )

        run_id = run.run_id if run else ""
        checks = list(
            db.scalars(select(QualityCheck).where(QualityCheck.run_id == run_id))
        )

        return {
            "incident_id": incident_id,
            "incident_status": incident.status if incident else "missing",
            "run_id": run.run_id if run else None,
            "open_dlq": db.scalar(
                select(func.count(DeadLetterMessage.id)).where(
                    DeadLetterMessage.incident_id == incident_id,
                    DeadLetterMessage.status == "open",
                )
            )
            or 0,
            "replayed_accepted_dlq": db.scalar(
                select(func.count(DeadLetterMessage.id)).where(
                    DeadLetterMessage.incident_id == incident_id,
                    DeadLetterMessage.status == "replayed_accepted",
                )
            )
            or 0,
            "replayed_failed_dlq": db.scalar(
                select(func.count(DeadLetterMessage.id)).where(
                    DeadLetterMessage.incident_id == incident_id,
                    DeadLetterMessage.status == "replayed_failed",
                )
            )
            or 0,
            "observations": db.scalar(select(func.count(Observation.id))) or 0,
            "duplicate_observation_source_message_ids": duplicate_sources,
            "audit_actions": sorted(actions),
            "quality_checks": [
                {"name": check.check_name, "status": check.status, "detail": check.detail}
                for check in checks
            ],
        }


def assert_replay_invariants(incident_id: str) -> dict[str, Any]:
    snapshot = replay_invariant_snapshot(incident_id)
    errors: list[str] = []

    if snapshot["incident_status"] != "remediated":
        errors.append(f"incident_status={snapshot['incident_status']}")

    if snapshot["open_dlq"] != 0:
        errors.append(f"open_dlq={snapshot['open_dlq']}")

    if snapshot["replayed_failed_dlq"] != 0:
        errors.append(f"replayed_failed_dlq={snapshot['replayed_failed_dlq']}")

    if snapshot["duplicate_observation_source_message_ids"]:
        errors.append(
            "duplicate observation source_message_id values: "
            + ", ".join(snapshot["duplicate_observation_source_message_ids"])
        )

    missing_actions = REQUIRED_AUDIT_ACTIONS - set(snapshot["audit_actions"])
    if missing_actions:
        errors.append("missing audit actions: " + ", ".join(sorted(missing_actions)))

    failed_checks = [
        check["name"] for check in snapshot["quality_checks"] if check["status"] != "passed"
    ]
    if failed_checks:
        errors.append("failed quality checks: " + ", ".join(failed_checks))

    if errors:
        raise AssertionError("; ".join(errors))

    return snapshot


def validate_incident_report(path: str | Path) -> dict[str, Any]:
    report_path = Path(path)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    missing = sorted(REQUIRED_REPORT_KEYS - set(report))
    if missing:
        raise AssertionError(f"{report_path} missing keys: {', '.join(missing)}")

    if report.get("no_phi") is not True:
        raise AssertionError(f"{report_path} must declare no_phi=true")

    run = report.get("run", {})
    if run.get("inbound") is None or run.get("accepted") is None:
        raise AssertionError(f"{report_path} run counts are incomplete")

    dlq = report.get("dlq", {})
    if "total" not in dlq or "open" not in dlq:
        raise AssertionError(f"{report_path} dlq counts are incomplete")

    warehouse = report.get("warehouse", {})
    if "observation_count" not in warehouse or "quality" not in warehouse:
        raise AssertionError(f"{report_path} warehouse proof is incomplete")

    return report


def write_replay_invariant_report(
    incident_id: str,
    output_path: str | Path = "evidence/replay-invariants.json",
) -> Path:
    snapshot = replay_invariant_snapshot(incident_id)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return path
