# Design notes

A few choices worth defending, and the boundaries that are deliberate.

## The integration run is the unit of work

Every message, failure, replay, and check is attached to a `run_id`. That is what
separates an operations tool from a dashboard: any number traces back to the record
that produced it and forward to what it affected.

## Failures are managed items, not exceptions

A rejected message becomes a dead-letter record with a category, a rule ID, and a
trace ID. Replay is a deliberate, audited action, not a silent retry of domain errors.

## The contract is data, not code

Required fields and rules live in `contracts/oru_contract.yml`. Changing the contract
changes validation without touching the engine, which is the point of a data contract.

## Identity resolution states its confidence

Exact MRN first, then a fuzzy demographic score that classifies probable matches,
possible duplicates for review, and unmatched records. It is demonstration-grade and
labelled as such, not an enterprise MPI.

## What I would harden for production

Enforce RBAC at the API, move from SQLite to Postgres, run dbt and a data-quality
framework for real, put the terminology map behind change review, and replace the
in-process loop with a broker so delivery and replay become platform concerns.
