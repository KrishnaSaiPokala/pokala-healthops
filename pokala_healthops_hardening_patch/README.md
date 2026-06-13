# Pokala HealthOps

Pokala HealthOps is a local-first, no-PHI healthcare interface reliability demo. It proves a controlled lab interface incident from ingest through dead-letter triage, terminology remediation, replay, warehouse verification, and evidence export.

Live site: https://krishnasaipokala.github.io/pokala-healthops/

Repository: https://github.com/KrishnaSaiPokala/pokala-healthops

## What this project proves

A synthetic ORU-style lab feed changes fasting glucose from `GLU_FAST` to `LAB:GLUCOSE_FASTING`. The new code is not in the active terminology map. Pokala HealthOps rejects the affected messages at the contract and mapping boundary, routes them to a dead-letter queue, opens an incident, applies a terminology fix, replays the failed records, verifies warehouse recovery, and exports an evidence package.

Measured demo outcome:

| Signal | Value |
| --- | ---: |
| Inbound ORU messages | 500 |
| Terminology failures | 218 |
| Accepted before replay | 282 |
| Recovered by replay | 218 |
| Final observations | 500 |
| Open DLQ after replay | 0 |
| Warehouse checks | 3 of 3 passed |

## Current status

| Capability | Status |
| --- | --- |
| ORU-style synthetic lab incident | Implemented |
| YAML contract required-field and timestamp checks | Implemented |
| Terminology mapping miss to DLQ | Implemented |
| Incident creation and replay | Implemented |
| Warehouse verification checks | Implemented |
| Incident report export | Implemented |
| FastAPI operational endpoints | Implemented |
| Prometheus metrics endpoint | Implemented, basic |
| Next.js command center | Visual MVP, static evidence backed after hardening patch |
| FHIR push to local HAPI | Optional, off by default |
| dbt, Airflow, Kubernetes | Scaffold or roadmap, not claimed as running |
| Real PHI, production EHR use, HIPAA certification | Out of scope |

See [STATUS.md](STATUS.md) for the detailed implemented versus roadmap table.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

python -m openhip.cli incident-demo
python -m openhip.cli replay-incident
python -m openhip.cli verify-warehouse
python -m openhip.cli export-incident-report
```

Or through Make:

```bash
make bootstrap
make incident-demo
make replay-incident
make verify-warehouse
make export-incident-report
make docs
```

Frontend:

```bash
cd apps/web
npm install
npm run typecheck
npm run build
```

## Architecture

```text
ORU feed
  -> contract validation
  -> terminology mapping
  -> demonstration MPI
  -> accepted observations
  -> warehouse verification
  -> evidence export

Rejected records
  -> dead-letter queue
  -> incident
  -> remediation
  -> replay
  -> audit trail
```

Every record that matters is tied to one or more of:

```text
run_id
trace_id
message_id
incident_id
dlq_id
```

## Evidence

The evidence package is the proof layer. It contains JSON reports, DLQ state before and after replay, quality checks, audit events, and metrics samples. See [docs/evidence.md](docs/evidence.md).

## Data policy

This project uses synthetic/demo data and small public reference samples only. It must not ingest, store, display, or process PHI, employer data, credentials, real patient records, or private operational data.

This is not a clinical system, not a medical device, and not a HIPAA certification claim.

## Design posture

The project is intentionally local-first. The public site is a portfolio and evidence surface. The operational service runs locally. Scaffolds are kept out of the main claims until they run under CI.
