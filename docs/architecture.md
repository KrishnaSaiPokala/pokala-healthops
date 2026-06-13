# Architecture

Pokala HealthOps is organized around one operational invariant:

> A failed interface message must be explainable, replayable, auditable, and verifiable.

## Flow

```text
synthetic ORU feed
  -> contract validation
  -> terminology mapping
  -> demonstration MPI
  -> accepted observation store
  -> warehouse checks
  -> evidence export

failed validation or mapping
  -> dead-letter message
  -> incident
  -> remediation
  -> replay
  -> audit
  -> verification
```

## Core objects

| Object | Purpose |
| --- | --- |
| `IntegrationRun` | Groups one interface run and its counts. |
| `RawMessage` | Captures inbound message payload, trace, and status. |
| `DeadLetterMessage` | Stores failed payload, rule ID, category, trace, and replay state. |
| `Incident` | Tracks operational failure, status, remediation, and closure. |
| `Observation` | Stores accepted lab results after mapping and MPI resolution. |
| `AuditEvent` | Records incident and replay activity. |
| `QualityCheck` | Stores warehouse verification results. |

## Reliability checks added

The project now includes replay invariant checks in `openhip/reliability.py`.

They verify:

- no open DLQ remains after replay
- no replay failures remain
- incident status is remediated
- observations are not duplicated by replay
- required audit actions exist
- warehouse checks pass

These checks are intentionally small and explicit. They are not a substitute for production operations, but they turn the portfolio demo from a happy-path script into a testable recovery workflow.

## Boundaries

Implemented:

- local SQLite-backed workflow
- FastAPI surface
- CLI demo flow
- evidence export
- static evidence-backed web dashboard
- public-reference sample enrichment

Not implemented as production systems:

- hosted ingestion
- real PHI handling
- HIPAA certification
- enterprise MPI
- real FHIR certification
- Kubernetes operations
- Airflow/dbt production pipelines
