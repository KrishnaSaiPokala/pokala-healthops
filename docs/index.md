# OpenHIP Command Center

A local-first control plane for healthcare interface operations. It receives an
HL7 ORU-style lab feed, checks each message against a versioned data contract,
resolves patient identity, maps the local lab code to a target code, and sends
anything that fails into a dead-letter queue that can be replayed once the
underlying problem is fixed.

Everything here runs on synthetic data. There is no PHI, no employer data, and
nothing hosted that accepts uploads.

## The incident this project is built around

A lab system changes its fasting-glucose code from `GLU_FAST` to
`LAB:GLUCOSE_FASTING`. The new code is not in the active map, so those results
stop loading. OpenHIP catches it at the contract boundary instead of letting it
fail silently downstream.

| Step | Result |
| --- | --- |
| ORU messages ingested | 500 |
| Rejected on the code change | 218 |
| Routed to dead-letter queue | 218 |
| Recovered after the map fix + replay | 218 |
| Open dead-letters afterwards | 0 |
| Warehouse checks passing | 3 / 3 |

## Run it

```bash
make bootstrap && source .venv/bin/activate
make incident-demo
make replay-incident
make verify-warehouse
make export-incident-report
```
