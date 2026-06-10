from pathlib import Path

path = Path("openhip/pipeline.py")
text = path.read_text(encoding="utf-8")

start = text.index("def replay_incident(")
end = text.index("\ndef verify_warehouse()", start)

new_func = r'''
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

            patient = db.scalar(
                select(Patient).where(Patient.mrn == parsed.get("patient_mrn", ""))
            )

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
            incident.closed_at = datetime.utcnow() if still_failed == 0 else None
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

'''

path.write_text(text[:start] + new_func + text[end:], encoding="utf-8")
print("Patched openhip/pipeline.py replay_incident successfully.")
