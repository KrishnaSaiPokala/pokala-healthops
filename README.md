# Pokala HealthOps

**Healthcare Interface Operations Platform**

Detect. Triage. Replay. Verify. Audit.

Pokala HealthOps is a no-PHI healthcare interface operations platform built to demonstrate production-style clinical data reliability workflows. It shows how healthcare integration teams manage interface failures from detection through recovery using synthetic data, contract validation, terminology mapping, dead-letter routing, incident remediation, replay, warehouse verification, observability, and audit evidence.

## Why This Project Exists

Healthcare interfaces fail in ways that are operationally expensive: lab code changes, malformed messages, missing mappings, patient identity mismatches, stale warehouse data, and unreplayed dead-letter queues. Pokala HealthOps turns that problem into a complete engineering demonstration.

This project is designed to show senior-level capability across:

- Health IT engineering
- Healthcare interoperability
- Interface operations
- Backend engineering
- Data platform engineering
- Observability and audit
- Incident response workflows

## No-PHI Guardrail

This project uses only synthetic demo data. Do not upload, paste, ingest, commit, or process real patient data, employer data, credentials, or secrets.

This project does not claim HIPAA certification, production clinical deployment readiness, enterprise MPI replacement, or real EHR integration.

## Flagship Incident Demo

A lab feed changes fasting glucose from `GLU_FAST` to `LAB:GLUCOSE_FASTING`.

Pokala HealthOps:

1. Ingests 500 synthetic ORU-style lab messages.
2. Detects 218 terminology mapping failures.
3. Routes failed messages to the dead-letter queue.
4. Opens an operational incident.
5. Applies a terminology map fix.
6. Replays the failed records.
7. Verifies warehouse recovery.
8. Produces audit and evidence artifacts.

Final verified state:

| Metric | Value |
|---|---:|
| Synthetic inbound messages | 500 |
| Initial terminology failures | 218 |
| Recovered after replay | 218 |
| Final observations | 500 |
| Open DLQ after replay | 0 |
| Warehouse checks | 3/3 passed |

## Fast Start

    python -m openhip.cli incident-demo
    python -m openhip.cli replay-incident
    python -m openhip.cli verify-warehouse
    python -m openhip.cli export-incident-report
    python -m mkdocs serve

## Core System Areas

- `openhip/pipeline.py` - ingestion, validation, DLQ, remediation, replay, verification
- `apps/api` - FastAPI operational API
- `apps/web` - dashboard scaffold
- `contracts` - interface contract definitions
- `docs` - public GitHub Pages site
- `reports` - generated incident evidence
- `tests` - automated regression checks

## Portfolio Signal

Pokala HealthOps is positioned for roles such as Health IT Engineer, Interface Engineer, Interoperability Engineer, Healthcare Data Engineer, Backend Engineer, Platform Engineer, and Solutions Engineer.
