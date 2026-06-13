# Pokala HealthOps

Pokala HealthOps is a local-first, no-PHI healthcare interface reliability demo. It proves one controlled lab-interface incident from ingest through triage, replay, verification, and evidence export.

## Demo outcome

| Signal | Value |
| --- | ---: |
| Inbound ORU messages | 500 |
| Terminology failures | 218 |
| Accepted before replay | 282 |
| Recovered by replay | 218 |
| Final observations | 500 |
| Open DLQ after replay | 0 |
| Warehouse checks | 3 of 3 passed |

## System boundary

This is not a production EHR system. It does not process PHI. It does not claim HIPAA certification. It demonstrates operational controls for a synthetic healthcare interface incident.

## Core flow

```text
Detect failed interface messages
  -> triage into DLQ
  -> open incident
  -> apply terminology fix
  -> replay failed records
  -> verify warehouse state
  -> export evidence
```

## What to inspect first

1. [Incident Demo](incident-demo.md)
2. [Evidence](evidence.md)
3. [Architecture](architecture.md)
4. [Security](security.md)
5. [Roadmap](roadmap.md)
