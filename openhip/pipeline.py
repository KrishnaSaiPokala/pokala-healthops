from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy import func, select

from openhip.contracts import load_contract, mapping_required, validate_structure
from openhip.db import SessionLocal, init_db, reset_db
from openhip.fhir import push_observation, to_observation_resource
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
from openhip.mpi import match_patient

INCIDENT_ID = "INC-20260602-LAB-CODE-FORMAT"
RUN_ID = "RUN-20260602-0001"
ORU_FIELDS = [
    "message_type", "patient_mrn", "patient_name", "patient_dob", "encounter_id",
    "observation_code", "observation_value", "observation_unit",
    "observation_datetime", "ordering_provider_id", "abnormal_flag",
]


def _trace() -> str:
    return uuid.uuid4().hex[:16]


def parse_oru(payload: str) -> dict[str, str]:
    return dict(zip(ORU_FIELDS, payload.split("|"), strict=False))


def build_oru_payload(i: int, bad_code: bool = False) -> str:
    code = "LAB:GLUCOSE_FASTING" if bad_code else "GLU_FAST"
    value = 80 + (i % 60)
    return "|".join([
        "ORU",
        f"MRN-{100000 + (i % 40):06d}",
        f"Demo Patient {i % 40:02d}",
        f"19{70 + (i % 25):02d}-01-{1 + (i % 27):02d}",
        f"ENC-{200000 + (i % 70):06d}",
        code,
        str(value),
        "mg/dL",
        "2026-06-02T09:00:00Z",
        "PRAC-0001",
        "H" if value > 120 else "N",
    ])


def seed_reference_data() -> None:
    init_db()
    with SessionLocal() as db:
        if db.scalar(select(func.count(Patient.id))) == 0:
            for i in range(40):
                db.add(Patient(
                    patient_id=f"PAT-{i:06d}",
                    mrn=f"MRN-{100000 + i:06d}",
                    name=f"Demo Patient {i:02d}",
                    dob=f"19{70 + (i % 25):02d}-01-{1 + (i % 27):02d}",
                    zip3=f"{210 + i % 20}",
                ))
        if db.scalar(select(func.count(Encounter.id))) == 0:
            for i in range(70):
                db.add(Encounter(
                    encounter_id=f"ENC-{200000 + i:06d}",
                    patient_id=f"PAT-{i % 40:06d}",
                ))
        if db.scalar(select(func.count(TerminologyMap.id))) == 0:
            db.add(TerminologyMap(
                source_code="GLU_FAST",
                source_display="fasting glucose",
                target_code="1558-6-demo",
                target_display="Glucose fasting [Mass/volume] in Serum or Plasma",
            ))
        db.commit()


def _dlq(db, run_id, msg_id, payload, parsed, trace, category, rule_id, error, incident_id):
    db.add(DeadLetterMessage(
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
        trace_id=trace,
        status="open",
    ))


def process_payload(db, run_id, msg_id, payload, incident_id=None) -> bool:
    parsed = parse_oru(payload)
    trace = _trace()
    contract = load_contract("oru_contract")
    db.add(RawMessage(
        run_id=run_id, message_id=msg_id, interface_name="lab_oru_feed",
        payload=payload, status="inbound", trace_id=trace,
    ))

    structural = validate_structure(parsed, contract)
    if structural is not None:
        _dlq(db, run_id, msg_id, payload, parsed, trace, *structural, incident_id)
        return False

    if mapping_required(contract):
        mapping = db.scalar(select(TerminologyMap).where(
            TerminologyMap.source_code == parsed["observation_code"],
            TerminologyMap.map_status == "active",
        ))
        if mapping is None:
            _dlq(
                db, run_id, msg_id, payload, parsed, trace,
                "terminology_mapping_failure", "ORU.OBS.CODE.MAP_REQUIRED",
                f"observation_code {parsed['observation_code']} not in active lab code map",
                incident_id,
            )
            return False
    else:
        mapping = None

    match = match_patient(
        db, parsed["patient_mrn"], parsed.get("patient_name", ""),
        parsed.get("patient_dob", ""),
    )
    if match.patient_id is None:
        _dlq(
            db, run_id, msg_id, payload, parsed, trace,
            "mpi_reference_failure", "ORU.PATIENT.MRN.RESOLVES",
            f"patient_mrn {parsed['patient_mrn']} did not resolve in synthetic MPI",
            incident_id,
        )
        return False

    observation = Observation(
        observation_id=f"OBS-{uuid.uuid4().hex[:10]}",
        run_id=run_id,
        source_message_id=msg_id,
        patient_id=match.patient_id,
        encounter_id=parsed["encounter_id"],
        source_code=parsed["observation_code"],
        target_code=mapping.target_code if mapping else "",
        target_display=mapping.target_display if mapping else "",
        value_numeric=float(parsed["observation_value"]),
        unit=parsed.get("observation_unit", "mg/dL"),
        abnormal_flag=parsed.get("abnormal_flag", "N"),
        observation_datetime=parsed["observation_datetime"],
        match_type=match.match_type,
        match_confidence=match.confidence,
    )
    db.add(observation)
    if mapping:
        push_observation(to_observation_resource(
            mapping.target_code, observation.value_numeric, observation.unit, match.patient_id,
        ))
    return True


def _audit(db, actor, role, action, resource_type, resource_id, outcome, run_id):
    db.add(AuditEvent(
        audit_event_id=f"AUD-{uuid.uuid4().hex[:8]}",
        actor_id=actor, role=role, action=action, resource_type=resource_type,
        resource_id=resource_id, outcome=outcome, run_id=run_id, trace_id=_trace(),
    ))


def demo_run(total: int = 100) -> dict:
    reset_db()
    seed_reference_data()
    with SessionLocal() as db:
        run = IntegrationRun(run_id="RUN-DEMO-0001", source_interface="lab_oru_feed",
                             source_type="hl7_v2_oru")
        db.add(run)
        db.commit()
        accepted = sum(
            process_payload(db, "RUN-DEMO-0001", f"MSG-{i:06d}", build_oru_payload(i))
            for i in range(total)
        )
        run.inbound_count = total
        run.accepted_count = accepted
        run.rejected_count = total - accepted
        run.reject_rate = (total - accepted) / total
        run.sla_status = "met" if run.reject_rate <= 0.02 else "breached"
        run.status = "completed"
        run.completed_at = datetime.utcnow()
        db.commit()
    return summarize()


def incident_demo(total: int = 500, bad_count: int = 218) -> dict:
    reset_db()
    seed_reference_data()
    with SessionLocal() as db:
        run = IntegrationRun(run_id=RUN_ID, source_interface="lab_oru_feed",
                             source_type="hl7_v2_oru")
        db.add(run)
        db.commit()
        accepted = 0
        for i in range(total):
            bad = i < bad_count
            accepted += process_payload(
                db, RUN_ID, f"MSG-ORU-{i:06d}", build_oru_payload(i, bad_code=bad),
                INCIDENT_ID if bad else None,
            )
        rejected = total - accepted
        db.add(Incident(
            incident_id=INCIDENT_ID, severity="medium", source_interface="lab_oru_feed",
            primary_failure="terminology_mapping_failure",
            failed_rule="ORU.OBS.CODE.MAP_REQUIRED", failed_messages=rejected,
        ))
        run.inbound_count = total
        run.accepted_count = accepted
        run.rejected_count = rejected
        run.reject_rate = rejected / total
        run.sla_status = "breached" if rejected / total > 0.02 else "met"
        run.status = "completed_with_failures"
        run.incident_id = INCIDENT_ID
        run.completed_at = datetime.utcnow()
        _audit(db, "system", "service", "incident_opened", "incident", INCIDENT_ID,
               "success", RUN_ID)
        db.commit()
    return summarize()


def _apply_mapping_fix(db) -> None:
    if db.scalar(select(TerminologyMap).where(
        TerminologyMap.source_code == "LAB:GLUCOSE_FASTING")) is None:
        db.add(TerminologyMap(
            source_code="LAB:GLUCOSE_FASTING",
            source_display="fasting glucose (new LIS format)",
            target_code="1558-6-demo",
            target_display="Glucose fasting [Mass/volume] in Serum or Plasma",
            version="lab_map_v2", updated_by="demo_analyst_01",
        ))


def replay_incident(incident_id: str = INCIDENT_ID) -> dict:
    init_db()
    with SessionLocal() as db:
        _apply_mapping_fix(db)
        db.flush()
        dlqs = list(db.scalars(select(DeadLetterMessage).where(
            DeadLetterMessage.incident_id == incident_id,
            DeadLetterMessage.status == "open",
        )))
        recovered = 0
        for dlq in dlqs:
            ok = process_payload(db, RUN_ID, f"REPLAY-{dlq.original_message_id}",
                                 dlq.raw_payload, incident_id)
            dlq.replay_count += 1
            dlq.last_replay_status = "accepted" if ok else "failed"
            dlq.status = "replayed_accepted" if ok else "replayed_failed"
            dlq.remediation_id = "REM-LAB-MAP-V2"
            recovered += int(ok)
        still_failed = len(dlqs) - recovered
        incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
        if incident:
            incident.status = "remediated" if still_failed == 0 else "partial"
            incident.closed_at = datetime.utcnow() if still_failed == 0 else None
            incident.remediation_summary = (
                f"Added LAB:GLUCOSE_FASTING map; replayed {len(dlqs)}; "
                f"recovered {recovered}; still failed {still_failed}."
            )
        _audit(db, "demo_analyst_01", "integration_engineer", "replay_completed",
               "incident", incident_id, "success" if still_failed == 0 else "partial", RUN_ID)
        db.commit()
    return summarize()


def verify_warehouse() -> dict:
    init_db()
    with SessionLocal() as db:
        db.query(QualityCheck).delete()
        obs = db.scalar(select(func.count(Observation.id))) or 0
        open_dlq = db.scalar(select(func.count(DeadLetterMessage.id)).where(
            DeadLetterMessage.status == "open")) or 0
        incident = db.scalar(select(Incident).where(Incident.incident_id == INCIDENT_ID))
        remediated = bool(incident and incident.status == "remediated")
        checks = [
            QualityCheck(run_id=RUN_ID, check_name="fact_observation_has_rows",
                         domain="warehouse", status="passed" if obs else "failed",
                         impacted_rows=0 if obs else 1, detail=f"observations={obs}"),
            QualityCheck(run_id=RUN_ID, check_name="open_deadletters_zero_after_replay",
                         domain="operations", status="passed" if open_dlq == 0 else "failed",
                         impacted_rows=open_dlq, detail=f"open_dlq={open_dlq}"),
            QualityCheck(run_id=RUN_ID, check_name="incident_remediated",
                         domain="incident", status="passed" if remediated else "failed",
                         impacted_rows=0 if remediated else 1,
                         detail=f"status={incident.status if incident else 'missing'}"),
        ]
        db.add_all(checks)
        db.commit()
        return {
            "total_checks": len(checks),
            "passed_checks": sum(c.status == "passed" for c in checks),
            "failed_checks": sum(c.status == "failed" for c in checks),
            "checks": [{"name": c.check_name, "status": c.status, "detail": c.detail}
                       for c in checks],
        }


def export_incident_report(incident_id: str = INCIDENT_ID) -> Path:
    init_db()
    Path("reports").mkdir(exist_ok=True)
    with SessionLocal() as db:
        incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
        run = db.scalar(select(IntegrationRun).where(IntegrationRun.incident_id == incident_id))
        dlq_total = db.scalar(select(func.count(DeadLetterMessage.id)).where(
            DeadLetterMessage.incident_id == incident_id)) or 0
        dlq_open = db.scalar(select(func.count(DeadLetterMessage.id)).where(
            DeadLetterMessage.incident_id == incident_id,
            DeadLetterMessage.status == "open")) or 0
        obs = db.scalar(select(func.count(Observation.id)).where(
            Observation.run_id == RUN_ID)) or 0
    report = {
        "incident_id": incident_id,
        "status": incident.status if incident else "missing",
        "primary_failure": incident.primary_failure if incident else "unknown",
        "failed_rule": incident.failed_rule if incident else "unknown",
        "failed_messages": incident.failed_messages if incident else 0,
        "remediation_summary": incident.remediation_summary if incident else None,
        "run": {
            "inbound": run.inbound_count if run else None,
            "accepted": run.accepted_count if run else None,
            "reject_rate": run.reject_rate if run else None,
        },
        "dlq": {"total": dlq_total, "open": dlq_open},
        "warehouse": {"observation_count": obs, "quality": verify_warehouse()},
        "no_phi": True,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    path = Path("reports") / f"{incident_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path


def mpi_demo() -> dict:
    """Exercise the MPI tiers on crafted synthetic inputs (no incident state)."""
    reset_db()
    seed_reference_data()
    cases = [
        ("MRN-100005", "Demo Patient 05", "exact MRN hit"),
        ("MRN-999999", "Demo Patient 07", "no MRN, strong name match"),
        ("MRN-999998", "Demo Patnt 11", "no MRN, fuzzy name"),
        ("MRN-999997", "Totally Different", "no plausible match"),
    ]
    results = []
    with SessionLocal() as db:
        for mrn, name, note in cases:
            m = match_patient(db, mrn, name)
            results.append({"input": note, "match_type": m.match_type,
                            "confidence": m.confidence, "review_required": m.review_required})
    return {"cases": results}


def summarize() -> dict:
    init_db()
    with SessionLocal() as db:
        return {
            "raw_messages": db.scalar(select(func.count(RawMessage.id))) or 0,
            "observations": db.scalar(select(func.count(Observation.id))) or 0,
            "dlq_total": db.scalar(select(func.count(DeadLetterMessage.id))) or 0,
            "dlq_open": db.scalar(select(func.count(DeadLetterMessage.id)).where(
                DeadLetterMessage.status == "open")) or 0,
            "incidents": db.scalar(select(func.count(Incident.id))) or 0,
            "audit_events": db.scalar(select(func.count(AuditEvent.id))) or 0,
        }
