# Project status

This file is the source of truth for public claims. Anything not listed as implemented is not claimed as working.

## Implemented

| Capability | Evidence |
| --- | --- |
| Synthetic ORU-style lab incident | CLI demo generates 500 messages and 218 terminology failures |
| YAML-driven contract checks | `contracts/oru_contract.yml` is loaded at validation time |
| Terminology mapping miss detection | `LAB:GLUCOSE_FASTING` fails until the map is updated |
| Dead-letter queue | Failed records are persisted with rule and trace context |
| Incident lifecycle | Incident opens on failure and remediates after replay |
| Replay after remediation | Failed records are reprocessed through the same pipeline |
| Warehouse verification | Three checks confirm observations, DLQ state, and incident status |
| Evidence export | Incident report JSON is produced by CLI |
| FastAPI endpoints | Summary, runs, incidents, DLQ, terminology, observations, metrics |
| Prometheus endpoint | Basic operational metrics are exposed at `/metrics` |
| MkDocs site | Published through GitHub Pages |
| CI quality gate | Lint, type check, tests, demo, replay, verification, docs build |

## Implemented but still thin

| Capability | Current limitation | Next hardening step |
| --- | --- | --- |
| Contract validation | Mostly required fields and timestamp checks | Add rule schema, type validation, severity, contract diff |
| Metrics | Counts and gauges only | Add counters, labels, histograms, SLO examples |
| Dashboard | Visual MVP | Back it with API or committed evidence JSON |
| Evidence | Export command exists | Commit evidence bundle and validate schemas in CI |
| Tests | Happy path coverage | Add idempotency, partial replay, malformed input, API error paths |
| Security | Honest no-PHI policy | Add threat model, scans, and data guardrails |

## Experimental or optional

| Capability | Status |
| --- | --- |
| Local HAPI FHIR push | Optional, off by default |
| Public reference-data enrichment | Planned |
| Browser-side incident explorer | Planned |
| Browser-side rule analyst | Planned |

## Scaffold or roadmap

| Capability | Status |
| --- | --- |
| dbt models | Scaffold only until compiled and tested in CI |
| Airflow DAG | Scaffold only until runnable locally and tested |
| Kubernetes manifests | Roadmap only unless deployed in a local cluster test |
| Full RBAC | Roadmap |
| OpenTelemetry tracing | Roadmap |
| Real-time streaming | Roadmap |

## Out of scope

| Item | Reason |
| --- | --- |
| PHI | Not needed and not safe for a public portfolio |
| Employer data | Not permitted |
| Production EHR integration | Outside the demo boundary |
| HIPAA certification claim | This project is not a compliance certification |
| Clinical decision support | The system is operational, not clinical |
