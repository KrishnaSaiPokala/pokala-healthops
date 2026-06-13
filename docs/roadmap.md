# Roadmap

The roadmap is ordered by credibility impact. Do not add new large surfaces before fixing proof gaps.

## 1. Evidence hardening

- Commit evidence bundle.
- Validate evidence JSON in CI.
- Expand evidence docs.
- Add screenshots only after they reflect real state.

## 2. Dashboard hardening

- Remove hardcoded operational metrics.
- Read static evidence JSON on the public site.
- Read FastAPI state in local mode.
- Add DLQ explorer and incident timeline.

## 3. Reliability tests

- Replay idempotency.
- Replay before remediation.
- Partial replay failure.
- Malformed payloads.
- Duplicate messages.
- Metrics matching database state.
- Audit event completeness.

## 4. Backend boundaries

- Split simulator, ingest, contracts, terminology, DLQ, incidents, audit, warehouse, metrics, and evidence.
- Keep `pipeline.py` as orchestration glue only.

## 5. Contract engine

- Add structured rule schema.
- Enforce field types.
- Add severity.
- Add contract diff report.
- Record contract version on failures.

## 6. Public reference enrichment

- Add small provider sample.
- Add small facility sample.
- Enrich dashboard and evidence.

## 7. Observability v2

- Add counters and labels.
- Add replay duration and DLQ age histograms.
- Add metric docs and alert examples.

## 8. FHIR decision

Choose one:

1. Keep FHIR clearly experimental.
2. Harden FHIR mapping, tests, failure handling, and docs.

No middle ground in public claims.
