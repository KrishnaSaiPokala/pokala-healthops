# Architecture

Each message carries a `run_id` and a `trace_id` from ingestion onward, so a
failure can be tied back to the exact record and forward to its downstream
effect.

```
ORU feed
  -> contract validation        (required fields, no future timestamps)
  -> terminology mapping         (local code -> target code)
  -> demonstration MPI           (exact, then fuzzy demographic tiers)
  -> accepted  -> observation store -> warehouse checks -> optional FHIR
  -> rejected  -> dead-letter queue -> incident -> replay -> verify
```

## Components

| Area | Implementation |
| --- | --- |
| Service | FastAPI |
| Storage | SQLAlchemy over SQLite (Postgres-ready) |
| Contracts | Versioned YAML, loaded at validation time |
| Identity | rapidfuzz demographic scoring |
| Metrics | prometheus-client `/metrics` endpoint |
| UI | Next.js dashboard |
| Docs | MkDocs Material on GitHub Pages |

The contract is the source of truth: required fields and rules live in
`contracts/oru_contract.yml`, not in code, so changing the contract changes
the validation behaviour.
