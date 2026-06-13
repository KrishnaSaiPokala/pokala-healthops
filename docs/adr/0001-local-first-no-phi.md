# ADR 0001: Local-first and no PHI

## Decision

Pokala HealthOps is local-first and uses synthetic/demo data plus small public reference samples only.

## Reason

A public portfolio project must be reproducible without private data, employer systems, paid services, or compliance risk.

## Consequences

- The core demo can run in CI.
- Evidence can be committed publicly.
- The project must not accept public uploads.
- Any production or compliance claim must be avoided.
