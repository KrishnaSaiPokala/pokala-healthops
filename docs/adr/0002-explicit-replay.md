# ADR 0002: Explicit replay instead of silent retry

## Decision

Domain failures are routed to DLQ and replayed only after remediation.

## Reason

A terminology failure is not an infrastructure retry problem. Retrying before a mapping fix only repeats the failure and hides operational work.

## Consequences

- DLQ records become managed work items.
- Replay requires an incident and remediation context.
- Audit events can prove who changed what and what recovered.
- Partial replay behavior must be tested before stronger reliability claims.
