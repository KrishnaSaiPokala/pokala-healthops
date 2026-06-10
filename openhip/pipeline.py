from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import uuid

from sqlalchemy import select, func

from openhip.db import SessionLocal, init_db, reset_db
from openhip.models import (
    AuditEvent,
    DeadLetterMessage,
    Encounter,
    Incident,
    IntegrationRun,
    Observation,
    Patient,
    QualityCheck,
    RawMessage,
    TerminologyMap,
)

INCIDENT_ID = "INC-20260602-LAB-CODE-FORMAT"
RUN_ID = "RUN-20260602-0001"


def trace_id() -> str:
    return uuid.uuid4().hex[:16]


def message_id(i: int) -> str:
    return f"MSG-ORU-{i:06d}"


def parse_oru(payload: str) -> dict[str, str]:
    fields = payload.split("|")
    keys = [
        "message_type",
        "patient_mrn",
        "patient_name",
        "patient_dob",
        "encounter_id",
        "observation_code",
        "observation_value",
        "observation_unit",
        "observation_datetime",
        "ordering_provider_id",
        "abnormal_flag",
    ]
    return dict(zip(keys, fields, strict=False))


def build_oru_payload(i: int, bad_code: bool = False) -> str:
    code = "LAB:GLUCOSE_FASTING" if bad_code else "GLU_FAST"
    mrn = f"MRN-{100000 + (i % 40):06d}"
    name = f"Demo Patient {i % 40:02d}"
    dob = f"19{70 + (i % 25):02d}-01-{1 + (i % 27):02d}"
    encounter = f"ENC-{200000 + (i % 70):06d}"
    value = str(80 + (i % 60))
    abnormal = "H" if int(value) > 120 else "N"
    return "|".join(
        [
            "ORU",
            mrn,
            name,
            dob,
            encounter,
            code,
            value,
            "mg/dL",
            "2026-06-02T09:00:00Z",
            "PRAC-0001",
            abnormal,
        ]
    )


def seed_reference_data() -> None:
    init_db()
    with SessionLocal() as db:
        if db.scalar(select(func.count(Patient.id))) == 0:
            for i in range(40):
                patient = Patient(
                    patient_id=f"PAT-{i:06d}",
                    mrn=f"MRN-{100000 + i:06d}",
                    name=f"Demo Patient {i:02d}",
                    dob=f"19{70 + (i % 25):02d}-01-{1 + (i % 27):02d}",
                    zip3=f"{210 + i % 20}",
                )
                db.add(patient)

        if db.scalar(select(func.count(Encounter.id))) == 0:
            for i in range(70):
                encounter = Encounter(
                    encounter_id=f"ENC-{200000 + i:06d}",
                    patient_id=f"PAT-{i % 40:06d}",
                    encounter_type="outpatient",
                    status="active",
                )
                db.add(encounter)

        if db.scalar(select(func.count(TerminologyMap.id))) == 0:
            db.add(
                TerminologyMap(
                    source_code="GLU_FAST",
                    source_display="fasting glucose",
                    target_code="1558-6-demo",
                    target_display="Glucose fasting [Mass/volume] in Serum or Plasma",
                )
            )

        db.commit()


def process_payload(
    db, run_id: str, msg_id: str, payload: str, incident_id: str | None = None
) -> bool:
    parsed = parse_oru(payload)
    t_id = trace_id()

    db.add(
        RawMessage(
            run_id=run_id,
            message_id=msg_id,
            interface_name="lab_oru_feed",
            source_type="hl7_v2_oru",
            payload=payload,
            status="inbound",
            trace_id=t_id,
        )
    )

    required = [
        "patient_mrn",
        "patient_dob",
        "encounter_id",
        "observation_code",
        "observation_value",
        "observation_unit",
        "observation_datetime",
    ]

    for field in required:
        if not parsed.get(field):
            create_dlq(
                db,
                run_id,
                msg_id,
                payload,
                parsed,
                t_id,
                "contract_schema_failure",
                f"ORU.REQUIRED.{field.upper()}",
                f"{field} is required",
                incident_id,
            )
            return False

    mapping = db.scalar(
        select(TerminologyMap).where(
            TerminologyMap.source_code == parsed["observation_code"],
            TerminologyMap.map_status == "active",
        )
    )

    if mapping is None:
        create_dlq(
            db,
            run_id,
            msg_id,
            payload,
            parsed,
            t_id,
            "terminology_mapping_failure",
            "ORU.OBS.CODE.MAP_REQUIRED",
            f"observation_code {parsed['observation_code']} not found in lab_code_map v1",
            incident_id,
        )
        return False

    patient = db.scalar(select(Patient).where(Patient.mrn == parsed["patient_mrn"]))
    if patient is None:
        create_dlq(
            db,
            run_id,
            msg_id,
            payload,
            parsed,
            t_id,
            "mpi_reference_failure",
            "ORU.PATIENT.MRN.RESOLVES",
            f"patient_mrn {parsed['patient_mrn']} not found in synthetic MPI",
            incident_id,
        )
        return False

    observation = Observation(
        observation_id=f"OBS-{uuid.uuid4().hex[:10]}",
        run_id=run_id,
        source_message_id=msg_id,
        patient_id=patient.patient_id,
        encounter_id=parsed["encounter_id"],
        source_code=parsed["observation_code"],
        target_code=mapping.target_code,
        target_display=mapping.target_display,
        value_numeric=float(parsed["observation_value"]),
        unit="mg/dL",
        abnormal_flag=parsed.get("abnormal_flag", "N"),
        observation_datetime=parsed["observation_datetime"],
        mapping_status="mapped",
        validation_status="accepted",
    )
    db.add(observation)
    return True


def create_dlq(
    db,
    run_id: str,
    msg_id: str,
    payload: str,
    parsed: dict[str, str],
    t_id: str,
    category: str,
    rule_id: str,
    error: str,
    incident_id: str | None,
) -> None:
    db.add(
        DeadLetterMessage(
            dlq_id=f"DLQ-{uuid.uuid4().hex[:10]}",
            original_message_id=msg_id,
            run_id=run_id,
            incident_id=incident_id,
            interface_name="lab_oru_feed",
            topic="mapping.failed" if "terminology" in category else "contract.failed",
            failure_category=category,
            failed_rule_id=rule_id,
            error_message=error,
            raw_payload=payload,
            patient_key=parsed.get("patient_mrn", "unknown"),
            trace_id=t_id,
            status="open",
        )
    )


def demo_run(total: int = 100) -> dict:
    reset_db()
    seed_reference_data()

    with SessionLocal() as db:
        run = IntegrationRun(
            run_id="RUN-DEMO-0001",
            source_interface="lab_oru_feed",
            source_type="hl7_v2_oru",
            status="running",
        )
        db.add(run)
        db.commit()

        accepted = 0
        rejected = 0
        for i in range(total):
            ok = process_payload(db, "RUN-DEMO-0001", message_id(i), build_oru_payload(i), None)
            accepted += int(ok)
            rejected += int(not ok)

        run.inbound_count = total
        run.accepted_count = accepted
        run.rejected_count = rejected
        run.reject_rate = rejected / total
        run.sla_status = "met" if run.reject_rate <= 0.02 else "breached"
        run.status = "completed"
        run.completed_at = datetime.now(UTC)
        db.commit()

        return summarize()


def incident_demo(total: int = 500, bad_count: int = 218) -> dict:
    reset_db()
    seed_reference_data()

    with SessionLocal() as db:
        run = IntegrationRun(
            run_id=RUN_ID,
            source_interface="lab_oru_feed",
            source_type="hl7_v2_oru",
            status="running",
        )
        db.add(run)
        db.commit()

        accepted = 0
        rejected = 0

        for i in range(total):
            bad = i < bad_count
            ok = process_payload(
                db,
                RUN_ID,
                message_id(i),
                build_oru_payload(i, bad_code=bad),
                INCIDENT_ID if bad else None,
            )
            accepted += int(ok)
            rejected += int(not ok)

        reject_rate = rejected / total

        incident = Incident(
            incident_id=INCIDENT_ID,
            severity="medium",
            source_interface="lab_oru_feed",
            primary_failure="terminology_mapping_failure",
            failed_rule="ORU.OBS.CODE.MAP_REQUIRED",
            failed_messages=rejected,
            status="open",
        )
        db.add(incident)

        run.inbound_count = total
        run.accepted_count = accepted
        run.rejected_count = rejected
        run.reject_rate = reject_rate
        run.sla_status = "breached" if reject_rate > 0.02 else "met"
        run.status = "completed_with_failures"
        run.incident_id = INCIDENT_ID
        run.completed_at = datetime.now(UTC)

        db.add(
            AuditEvent(
                audit_event_id=f"AUD-{uuid.uuid4().hex[:8]}",
                actor_id="system",
                role="service",
                action="incident_opened",
                resource_type="incident",
                resource_id=INCIDENT_ID,
                outcome="success",
                run_id=RUN_ID,
                trace_id=trace_id(),
            )
        )

        db.commit()
        return summarize()


def apply_mapping_fix(db) -> None:
    existing = db.scalar(
        select(TerminologyMap).where(TerminologyMap.source_code == "LAB:GLUCOSE_FASTING")
    )
    if existing is None:
        db.add(
            TerminologyMap(
                source_code="LAB:GLUCOSE_FASTING",
                source_display="fasting glucose new LIS format",
                target_code="1558-6-demo",
                target_display="Glucose fasting [Mass/volume] in Serum or Plasma",
                version="lab_map_v2",
                updated_by="demo_analyst_01",
            )
        )


def replay_incident(incident_id: str = INCIDENT_ID) -> dict:
    """
    Replay open DLQ messages after remediation.

    Correct behavior:
    - Add the missing terminology mapping.
    - Reprocess only currently open DLQ records.
    - Create recovered observations directly from original raw payloads.
    - Mark original DLQ rows as replayed_accepted.
    - Do not create duplicate/new DLQ rows during successful replay.
    - Close the incident when all replayed messages recover.
    """
    init_db()

    with SessionLocal() as db:
        apply_mapping_fix(db)
        db.flush()

        dlqs = list(
            db.scalars(
                select(DeadLetterMessage).where(
                    DeadLetterMessage.incident_id == incident_id,
                    DeadLetterMessage.status == "open",
                )
            ).all()
        )

        recovered = 0
        still_failed = 0

        for dlq in dlqs:
            parsed = parse_oru(dlq.raw_payload)
            replay_trace_id = trace_id()

            mapping = db.scalar(
                select(TerminologyMap).where(
                    TerminologyMap.source_code == parsed.get("observation_code", ""),
                    TerminologyMap.map_status == "active",
                )
            )

            patient = db.scalar(select(Patient).where(Patient.mrn == parsed.get("patient_mrn", "")))

            if mapping is not None and patient is not None:
                replay_message_id = f"REPLAY-{dlq.original_message_id}"

                db.add(
                    RawMessage(
                        run_id=RUN_ID,
                        message_id=replay_message_id,
                        interface_name="lab_oru_feed",
                        source_type="hl7_v2_oru",
                        payload=dlq.raw_payload,
                        status="replayed",
                        trace_id=replay_trace_id,
                    )
                )

                db.add(
                    Observation(
                        observation_id=f"OBS-RPLY-{uuid.uuid4().hex[:10]}",
                        run_id=RUN_ID,
                        source_message_id=replay_message_id,
                        patient_id=patient.patient_id,
                        encounter_id=parsed["encounter_id"],
                        source_code=parsed["observation_code"],
                        target_code=mapping.target_code,
                        target_display=mapping.target_display,
                        value_numeric=float(parsed["observation_value"]),
                        unit="mg/dL",
                        abnormal_flag=parsed.get("abnormal_flag", "N"),
                        observation_datetime=parsed["observation_datetime"],
                        mapping_status="mapped_after_replay",
                        validation_status="accepted",
                    )
                )

                dlq.status = "replayed_accepted"
                dlq.replay_count += 1
                dlq.last_replay_status = "accepted"
                dlq.remediation_id = "REM-LAB-MAP-V2"
                recovered += 1

            else:
                dlq.replay_count += 1
                dlq.last_replay_status = "failed"
                dlq.status = "open"
                still_failed += 1

        incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
        if incident:
            incident.status = "remediated" if still_failed == 0 else "partial"
            incident.closed_at = datetime.now(UTC) if still_failed == 0 else None
            incident.remediation_summary = (
                f"Added LAB:GLUCOSE_FASTING mapping; replayed {len(dlqs)} DLQ messages; "
                f"recovered {recovered}; still failed {still_failed}."
            )

        run = db.scalar(select(IntegrationRun).where(IntegrationRun.incident_id == incident_id))
        if run:
            run.accepted_count += recovered
            run.status = "recovered" if still_failed == 0 else "completed_with_partial_recovery"
            run.sla_status = "recovered" if still_failed == 0 else "breached"

        db.add(
            AuditEvent(
                audit_event_id=f"AUD-{uuid.uuid4().hex[:8]}",
                actor_id="demo_analyst_01",
                role="integration_engineer",
                action="replay_request_completed",
                resource_type="incident",
                resource_id=incident_id,
                outcome="success" if still_failed == 0 else "partial",
                run_id=RUN_ID,
                trace_id=trace_id(),
            )
        )

        db.commit()
        return summarize()


def verify_warehouse() -> dict:
    init_db()
    with SessionLocal() as db:
        db.query(QualityCheck).delete()

        observations = db.scalar(select(func.count(Observation.id))) or 0
        open_dlq = (
            db.scalar(
                select(func.count(DeadLetterMessage.id)).where(DeadLetterMessage.status == "open")
            )
            or 0
        )
        incident = db.scalar(select(Incident).where(Incident.incident_id == INCIDENT_ID))

        checks = [
            QualityCheck(
                run_id=RUN_ID,
                check_name="fact_observation_has_rows",
                domain="warehouse",
                status="passed" if observations > 0 else "failed",
                impacted_rows=0 if observations > 0 else 1,
                detail=f"observations={observations}",
            ),
            QualityCheck(
                run_id=RUN_ID,
                check_name="deadletter_open_count_zero_after_replay",
                domain="operations",
                status="passed" if open_dlq == 0 else "failed",
                impacted_rows=open_dlq,
                detail=f"open_dlq={open_dlq}",
            ),
            QualityCheck(
                run_id=RUN_ID,
                check_name="incident_remediated",
                domain="incident",
                status="passed" if incident and incident.status == "remediated" else "failed",
                impacted_rows=0 if incident and incident.status == "remediated" else 1,
                detail=f"incident_status={incident.status if incident else 'missing'}",
            ),
        ]

        db.add_all(checks)
        db.commit()

        return {
            "total_checks": len(checks),
            "passed_checks": sum(c.status == "passed" for c in checks),
            "failed_checks": sum(c.status == "failed" for c in checks),
            "checks": [
                {
                    "name": c.check_name,
                    "domain": c.domain,
                    "status": c.status,
                    "detail": c.detail,
                }
                for c in checks
            ],
        }


def export_incident_report(incident_id: str = INCIDENT_ID) -> Path:
    init_db()
    Path("reports").mkdir(exist_ok=True)

    with SessionLocal() as db:
        incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
        run = db.scalar(select(IntegrationRun).where(IntegrationRun.incident_id == incident_id))
        dlq_total = db.scalar(
            select(func.count(DeadLetterMessage.id)).where(
                DeadLetterMessage.incident_id == incident_id
            )
        )
        dlq_open = db.scalar(
            select(func.count(DeadLetterMessage.id)).where(
                DeadLetterMessage.incident_id == incident_id,
                DeadLetterMessage.status == "open",
            )
        )
        obs_count = db.scalar(
            select(func.count(Observation.id)).where(Observation.run_id == RUN_ID)
        )
        quality = verify_warehouse()

        report = {
            "incident_id": incident_id,
            "severity": incident.severity if incident else "unknown",
            "status": incident.status if incident else "missing",
            "source_interface": incident.source_interface if incident else "unknown",
            "primary_failure": incident.primary_failure if incident else "unknown",
            "failed_rule": incident.failed_rule if incident else "unknown",
            "failed_messages": incident.failed_messages if incident else 0,
            "remediation_summary": incident.remediation_summary if incident else None,
            "run": {
                "run_id": run.run_id if run else None,
                "inbound_count": run.inbound_count if run else None,
                "accepted_count": run.accepted_count if run else None,
                "rejected_count": run.rejected_count if run else None,
                "reject_rate": run.reject_rate if run else None,
                "sla_status": run.sla_status if run else None,
            },
            "dlq": {
                "total": dlq_total,
                "open": dlq_open,
            },
            "warehouse": {
                "observation_count": obs_count,
                "quality": quality,
            },
            "no_phi": True,
            "generated_at": datetime.now(UTC).isoformat() + "Z",
        }

        path = Path("reports") / f"{incident_id}.json"
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return path


def summarize() -> dict:
    init_db()
    with SessionLocal() as db:
        return {
            "runs": db.scalar(select(func.count(IntegrationRun.id))) or 0,
            "raw_messages": db.scalar(select(func.count(RawMessage.id))) or 0,
            "observations": db.scalar(select(func.count(Observation.id))) or 0,
            "dlq_total": db.scalar(select(func.count(DeadLetterMessage.id))) or 0,
            "dlq_open": db.scalar(
                select(func.count(DeadLetterMessage.id)).where(DeadLetterMessage.status == "open")
            )
            or 0,
            "incidents": db.scalar(select(func.count(Incident.id))) or 0,
            "audit_events": db.scalar(select(func.count(AuditEvent.id))) or 0,
        }


def prometheus_metrics() -> str:
    init_db()
    with SessionLocal() as db:
        total = db.scalar(select(func.count(RawMessage.id))) or 0
        rejected = db.scalar(select(func.count(DeadLetterMessage.id))) or 0
        accepted = db.scalar(select(func.count(Observation.id))) or 0
        open_dlq = (
            db.scalar(
                select(func.count(DeadLetterMessage.id)).where(DeadLetterMessage.status == "open")
            )
            or 0
        )
        replayed = (
            db.scalar(
                select(func.count(DeadLetterMessage.id)).where(
                    DeadLetterMessage.status == "replayed_accepted"
                )
            )
            or 0
        )

    reject_rate = rejected / total if total else 0.0
    replay_success_rate = replayed / rejected if rejected else 0.0

    return "\n".join(
        [
            "# HELP openhip_interface_messages_total Total interface messages.",
            "# TYPE openhip_interface_messages_total counter",
            f'openhip_interface_messages_total{{interface="lab_oru_feed",status="inbound"}} {total}',
            f'openhip_interface_messages_total{{interface="lab_oru_feed",status="accepted"}} {accepted}',
            f'openhip_interface_messages_total{{interface="lab_oru_feed",status="rejected"}} {rejected}',
            "# HELP openhip_contract_reject_rate Contract reject rate.",
            "# TYPE openhip_contract_reject_rate gauge",
            f'openhip_contract_reject_rate{{interface="lab_oru_feed",contract="oru_v1"}} {reject_rate}',
            "# HELP openhip_deadletter_open_total Open DLQ messages.",
            "# TYPE openhip_deadletter_open_total gauge",
            f'openhip_deadletter_open_total{{interface="lab_oru_feed",category="terminology_mapping"}} {open_dlq}',
            "# HELP openhip_replay_success_rate Replay success rate.",
            "# TYPE openhip_replay_success_rate gauge",
            f'openhip_replay_success_rate{{incident_id="{INCIDENT_ID}"}} {replay_success_rate}',
            "",
        ]
    )
