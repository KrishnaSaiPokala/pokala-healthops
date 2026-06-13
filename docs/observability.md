# Observability

The project exposes operational state through the database, API endpoints, evidence files, and Prometheus-formatted metrics.

## Current signals

| Signal | Source |
| --- | --- |
| inbound count | `IntegrationRun.inbound_count` |
| accepted count | `IntegrationRun.accepted_count` |
| rejected count | `IntegrationRun.rejected_count` |
| open DLQ | `DeadLetterMessage.status = open` |
| replayed DLQ | `DeadLetterMessage.status = replayed_accepted` |
| incident status | `Incident.status` |
| warehouse checks | `QualityCheck` |
| audit actions | `AuditEvent.action` |

## Reliability invariant report

Run:

```bash
python -m openhip.cli verify-replay-invariants
```

The command writes:

```text
evidence/replay-invariants.json
```

The report is useful because it checks the actual database state after replay instead of trusting console output.

## Metrics roadmap

The current metrics endpoint is intentionally small. The next production-style increment is label-based counters and histograms:

```text
openhip_interface_messages_total{interface,status}
openhip_contract_violations_total{rule_id,category}
openhip_dlq_open_total{category}
openhip_replay_records_total{status}
openhip_incidents_total{status}
openhip_warehouse_checks_total{check,status}
```

Those should be added only when backed by tests.
