# Pokala HealthOps

Local-first, no-PHI healthcare interface reliability demo.

Pokala HealthOps proves one operational workflow end to end: a lab interface changes an observation code, messages fail contract/terminology checks, failures route to a dead-letter queue, a terminology fix is applied, failed messages are replayed, warehouse checks verify recovery, and evidence is exported.

## What runs

| Capability | Status |
| --- | --- |
| ORU-style synthetic lab ingest | Implemented |
| YAML contract validation | Implemented |
| Terminology mapping failure | Implemented |
| DLQ routing | Implemented |
| Incident creation | Implemented |
| Replay after terminology fix | Implemented |
| Warehouse verification | Implemented |
| Audit events | Implemented |
| Evidence export | Implemented |
| Replay invariant checks | Implemented |
| Public-reference provider enrichment sample | Implemented |
| FastAPI summary and operations endpoints | Implemented |
| Static evidence-backed Next.js dashboard | Implemented |
| FHIR push | Optional, local only, off by default |
| dbt / Airflow / Kubernetes | Roadmap or scaffold, not claimed as running production features |

## Flagship incident

`GLU_FAST` changes to `LAB:GLUCOSE_FASTING`.

| Metric | Value |
| --- | ---: |
| inbound ORU messages | 500 |
| terminology failures | 218 |
| accepted before replay | 282 |
| recovered by replay | 218 |
| final observations | 500 |
| open DLQ after replay | 0 |
| warehouse checks | 3 / 3 passed |

## Local verification

Windows PowerShell:

```powershell
python -m pip install -e ".[dev]"

ruff check .
mypy openhip apps/api
pytest -q

python -m openhip.cli incident-demo
python -m openhip.cli replay-incident
python -m openhip.cli verify-warehouse
python -m openhip.cli verify-replay-invariants
python -m openhip.cli export-incident-report

mkdocs build --strict
cd apps\web
npm install
npm run typecheck
npm run build
```

Linux/macOS:

```bash
make check
make incident-demo
make replay-incident
make verify-warehouse
python -m openhip.cli verify-replay-invariants
make export-incident-report
make docs
make web-build
```

## Evidence

Evidence files live under `evidence/`. Runtime reports are generated under `reports/` and `evidence/`.

Important files:

```text
evidence/incident-report.json
evidence/quality-checks.json
evidence/dlq-before.json
evidence/dlq-after.json
evidence/audit-events.json
evidence/metrics-sample.prom
evidence/replay-invariants.json
```

## Public data posture

The incident itself is synthetic so recovery is deterministic and safe to publish. Public-reference data is used only for non-patient context. The current sample is:

```text
data/public/provider_reference_sample.csv
```

## Safety boundary

This repository does not process PHI. It does not accept hosted uploads. It is not a clinical decision support system. It does not claim HIPAA certification.
