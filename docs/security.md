# Security and data policy

## Data boundary

Pokala HealthOps uses synthetic/demo data and small public reference samples only.

Do not use:

- PHI
- employer data
- credentials
- private logs
- real EHR exports
- real patient screenshots
- production operational data

## Deployment boundary

The public site is static documentation and evidence. It must not accept uploads. The API is intended for local demo use unless separately reviewed.

## Audit model

Audit events should record:

| Field | Meaning |
| --- | --- |
| `event_type` | What happened |
| `run_id` | Which run was affected |
| `incident_id` | Which incident was affected |
| `trace_id` | Which trace was affected, when available |
| `actor` | Demo actor or system actor |
| `created_at` | Timestamp |

Required audit events for the core incident:

1. Incident opened.
2. Terminology remediation applied.
3. Replay requested.
4. Replay completed.
5. Warehouse verification executed.
6. Evidence exported.

## Compliance boundary

This project is not a HIPAA certification claim. It is not a clinical system. It is not clinical decision support.

## Hardening backlog

1. Add `SECURITY.md`.
2. Add secret scanning.
3. Add CodeQL.
4. Add dependency updates through Dependabot.
5. Add no-PHI fixture scanner.
6. Add a threat model page.
