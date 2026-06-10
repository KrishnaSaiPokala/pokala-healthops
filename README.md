# OpenHIP Command Center

A local-first, no-PHI control plane for healthcare interface operations. It
ingests HL7 ORU-style lab feeds, validates them against a versioned data
contract, resolves patient identity, maps local lab codes to a target code
system, and routes anything that fails into a dead-letter queue that can be
inspected, remediated, and replayed. Every record is tied to a `run_id`.

The repository exists to demonstrate how an interface team detects, triages,
fixes, replays, and proves recovery of a healthcare integration incident.

## Run the incident in one minute

```bash
make bootstrap
source .venv/bin/activate
make incident-demo            # 500 ORU messages, 218 fail a code-format change
make replay-incident          # add the missing map, replay, recover all 218
make verify-warehouse         # three quality checks, all green
make export-incident-report   # JSON evidence in reports/
```

## What runs today vs. what is planned

This distinction is kept honest on purpose; see `docs/status.md`.

**Implemented:** contract-driven ORU validation, demonstration MPI with
deterministic + fuzzy tiers, dead-letter queue, replay engine, incident
lifecycle, audit events, warehouse quality checks, JSON evidence export,
Prometheus metrics, FastAPI service, a small web dashboard, CI, and tests.

**Optional / off by default:** pushing accepted results to a local HAPI FHIR
server (set `OPENHIP_FHIR_PUSH=true` with HAPI running).

**Scaffolded, not claimed as working:** dbt models, an Airflow DAG, and
Kubernetes manifests are included as structure, not as a running platform.

## No-PHI policy

Synthetic data only. Do not ingest, paste, or commit real patient data,
credentials, or employer data. This is not a clinical system, not a medical
device, and not a HIPAA compliance certification.

## Layout

```
apps/api      FastAPI service
apps/web      Next.js dashboard
openhip/      pipeline, contracts, mpi, metrics, fhir, cli
contracts/    versioned YAML interface contracts
docs/         MkDocs site published to GitHub Pages
tests/        pytest suite mirrored by CI
```
