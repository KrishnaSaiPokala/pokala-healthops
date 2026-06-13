# Incident demo

## Scenario

A lab system changes fasting glucose from `GLU_FAST` to `LAB:GLUCOSE_FASTING`. The new code is not in the active map.

## Expected behavior

The system should reject the affected records, keep accepted records flowing, group failures under one incident, allow remediation, replay only the failed records, and prove recovery.

## Steps

1. Ingest 500 synthetic ORU-style messages.
2. Validate each message against the ORU contract.
3. Reject 218 messages because `LAB:GLUCOSE_FASTING` is not mapped.
4. Route rejected messages to DLQ with rule `ORU.OBS.CODE.MAP_REQUIRED`.
5. Open incident `INC-20260602-LAB-CODE-FORMAT`.
6. Add the new terminology map.
7. Replay open DLQ records through the same pipeline.
8. Verify that final observations equal 500.
9. Verify open DLQ equals 0.
10. Verify the incident is remediated.
11. Export the incident report.

## Commands

```bash
python -m openhip.cli incident-demo
python -m openhip.cli replay-incident
python -m openhip.cli verify-warehouse
python -m openhip.cli export-incident-report
```

## Result

| Stage | Count |
| --- | ---: |
| Inbound messages | 500 |
| Rejected before remediation | 218 |
| Accepted before replay | 282 |
| Replayed after remediation | 218 |
| Final observations | 500 |
| Open DLQ after replay | 0 |
| Warehouse checks | 3 passed |

## What this proves

1. The system catches a terminology break at the integration boundary.
2. Failures are managed records, not lost messages.
3. Replay is explicit.
4. Recovery is verified.
5. Evidence can be exported.

## What this does not prove yet

1. Concurrent replay safety.
2. Partial replay recovery behavior.
3. Production-grade FHIR validation.
4. Real EHR integration.
5. HIPAA compliance.
