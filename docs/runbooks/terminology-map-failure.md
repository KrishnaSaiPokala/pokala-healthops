# Runbook: terminology map failure

## Symptom

A lab interface produces a spike in failures for rule `ORU.OBS.CODE.MAP_REQUIRED`.

## Likely cause

The sending system changed a local observation code and the receiving map has not been updated.

## Triage

1. Check reject count by rule.
2. Group DLQ records by source code.
3. Confirm that accepted records continue to flow.
4. Confirm affected assets.
5. Confirm no unrelated contract failures are present.

## Remediation

1. Add or activate the correct terminology mapping.
2. Record map version.
3. Record actor.
4. Mark the incident ready for replay.

## Replay safety

Replay must be explicit. Do not silently retry domain failures.

Replay should record:

- incident ID
- replay attempt ID
- DLQ IDs attempted
- success count
- failure count
- actor
- timestamp

## Verification

The incident is remediated only if:

1. Final observation count equals expected count.
2. Open DLQ equals zero for the incident.
3. Warehouse checks pass.
4. Audit events show remediation and replay.
5. Evidence export exists.

## Rollback

If replay creates bad observations, mark the replay attempt failed and leave the incident open. Do not hide partial recovery.
