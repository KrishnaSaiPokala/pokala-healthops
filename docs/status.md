# Status

Kept honest so the claims match the code.

## Implemented and tested

- Contract-driven ORU validation from YAML
- Demonstration MPI with exact and fuzzy tiers (rapidfuzz)
- Dead-letter queue, replay engine, incident lifecycle
- Warehouse quality checks and JSON evidence export
- Audit events, Prometheus metrics, FastAPI service, web dashboard
- CI running ruff, mypy, pytest, and the full demo on every push

## Optional, off by default

- Pushing accepted results to a local HAPI FHIR server
  (`OPENHIP_FHIR_PUSH=true`)

## Scaffolded, not yet a running platform

- dbt models, an Airflow DAG, Kubernetes manifests

## Deliberately out of scope

- Real patient data, HIPAA certification, enterprise MPI, a clinical assistant
