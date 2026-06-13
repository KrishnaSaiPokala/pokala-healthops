# Observability

The current metrics endpoint is a basic proof. The hardening target is an operational metric set that explains volume, failure type, replay behavior, DLQ state, and verification state.

## Current metric intent

| Signal | Meaning |
| --- | --- |
| Inbound messages | Interface volume |
| Accepted observations | Successful processing |
| Rejected messages | Contract or mapping failures |
| Open DLQ | Unresolved operational work |
| Reject rate | Interface health signal |

## Target metric set

```text
openhip_interface_messages_total{interface,status}
openhip_contract_violations_total{rule_id,category}
openhip_dlq_open_total{category}
openhip_replay_attempts_total{status}
openhip_replay_records_total{status}
openhip_incidents_total{status}
openhip_mpi_matches_total{tier}
openhip_warehouse_checks_total{check,status}
openhip_evidence_exports_total{status}
openhip_ingest_duration_seconds
openhip_replay_duration_seconds
openhip_dlq_age_seconds
```

## Alert examples

| Condition | Meaning |
| --- | --- |
| Reject rate above contract SLA | Interface may have changed format or code system |
| Open DLQ above zero after replay | Recovery incomplete |
| Replay failures above zero | Remediation did not cover all failed records |
| Warehouse check failure | Recovery is not proven |

## Evidence rule

A metrics sample should be committed under `evidence/metrics-sample.prom` and regenerated after the demo when possible.
