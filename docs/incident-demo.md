# Lab ORU Code-Format Incident

## Scenario

Source lab system changes fasting glucose code from `GLU_FAST`
to `LAB:GLUCOSE_FASTING`.

## Flow

1. Ingest ORU messages.
2. Validate contract.
3. Fail terminology mapping.
4. Route to DLQ.
5. Open incident.
6. Add terminology map.
7. Replay DLQ records.
8. Verify warehouse.
9. Export incident evidence.
