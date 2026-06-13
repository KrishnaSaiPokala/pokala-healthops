# Architecture

The system is built around one operational object: an integration run. Every message, accepted observation, dead-letter record, replay event, check, and evidence artifact must tie back to a run, trace, message, or incident identifier.

## Flow

```text
ORU feed
  -> contract validation
  -> terminology mapping
  -> demonstration MPI
  -> accepted observations
  -> warehouse checks
  -> evidence export

Rejected messages
  -> dead-letter queue
  -> incident
  -> remediation
  -> replay
  -> audit trail
```

## Identifiers

| Identifier | Purpose |
| --- | --- |
| `run_id` | Groups one ingest and recovery workflow |
| `trace_id` | Follows a message through validation, DLQ, replay, and evidence |
| `message_id` | Identifies the source message |
| `incident_id` | Groups failures under an operational incident |
| `dlq_id` | Identifies a rejected message that needs review or replay |

## Components

| Area | Current implementation | Hardening target |
| --- | --- | --- |
| API | FastAPI | Add error-path tests and clearer response models |
| Storage | SQLAlchemy over SQLite | Add migrations before claiming production readiness |
| Contracts | YAML loaded at validation time | Add rule schema, severity, and contract diff |
| Terminology | Local mapping table | Add inactive map tests and remediation audit |
| MPI | Demonstration exact and fuzzy matching | Add review-required outcomes and threshold tests |
| DLQ | Persisted failed messages | Add state machine and replay attempt records |
| Replay | Explicit replay after map fix | Add idempotency and partial-failure behavior |
| Metrics | Prometheus endpoint | Add counters, labels, histograms, and SLO examples |
| Evidence | JSON incident report | Add full evidence bundle and schema validation |
| UI | Next.js command center | Read API state or static evidence JSON |

## Design choices

### Local-first

Local-first keeps the demo reproducible and safe. The public site shows documentation and evidence. It does not host PHI or accept uploads.

### Explicit replay

Domain failures are not silently retried. A failed message becomes a managed DLQ item. Replay happens after a remediation action and is recorded in the audit trail.

### Synthetic core

Synthetic messages make the incident deterministic. Public reference data can enrich the demo, but it should not replace the controlled recovery path.

## Known limitations

1. The current contract engine is intentionally small.
2. The current dashboard must not be treated as a production control plane.
3. FHIR push is optional and off by default.
4. dbt, Airflow, and Kubernetes are roadmap or scaffold unless their workflows run in CI.
