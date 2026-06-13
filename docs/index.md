# Pokala HealthOps

Pokala HealthOps is a local-first healthcare interface reliability project. It demonstrates a controlled lab-interface failure and proves recovery through contract validation, dead-letter routing, replay, warehouse checks, audit events, and evidence files.

The project uses synthetic interface messages and small public-reference samples. It does not process PHI, does not accept hosted uploads, and does not claim HIPAA certification.

## What this proves

| Capability | Proof |
| --- | --- |
| Contract-driven validation | ORU messages are checked against `contracts/oru_contract.yml`. |
| Terminology failure handling | `LAB:GLUCOSE_FASTING` misses the active map and routes to DLQ. |
| Dead-letter operations | Failed payloads are stored with rule ID, category, trace, and incident. |
| Explicit replay | Remediation adds the missing terminology map before replay. |
| Recovery verification | Warehouse checks assert observations exist, DLQ is closed, and incident is remediated. |
| Audit trail | Incident opening and replay completion are written as audit events. |
| Evidence | JSON reports and sample Prometheus metrics are committed under `evidence/`. |
| Public-reference context | A small provider-reference sample shows how synthetic interface events can be enriched without PHI. |

## Flagship incident

A lab feed changes fasting glucose from `GLU_FAST` to `LAB:GLUCOSE_FASTING`.

| Stage | Result |
| --- | ---: |
| ORU messages ingested | 500 |
| Mapping failures | 218 |
| Accepted before replay | 282 |
| Replayed after terminology fix | 218 |
| Final observations | 500 |
| Open DLQ after replay | 0 |
| Warehouse checks | 3 / 3 passed |

## Engineering posture

This is not a production healthcare system. It is a portfolio system built to show reliability engineering judgment around healthcare interfaces:

- data contracts
- failure taxonomy
- DLQ and replay
- incident lifecycle
- audit events
- metrics
- warehouse verification
- evidence generation
- public-reference enrichment
- no-PHI boundaries

The roadmap keeps scaffolded areas separate from implemented behavior.
