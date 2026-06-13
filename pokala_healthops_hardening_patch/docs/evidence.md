# Evidence

Evidence is the proof layer for the incident. It must answer six questions:

1. What arrived?
2. What failed?
3. Why did it fail?
4. What changed?
5. What was replayed?
6. How was recovery verified?

## Evidence files

| File | Purpose |
| --- | --- |
| `evidence/incident-report.json` | Incident summary, before and after counts, run context |
| `evidence/dlq-before.json` | DLQ state before remediation |
| `evidence/dlq-after.json` | DLQ state after replay |
| `evidence/quality-checks.json` | Warehouse verification results |
| `evidence/audit-events.json` | Operational audit trail |
| `evidence/metrics-sample.prom` | Prometheus sample output |
| `evidence/README.md` | Evidence package notes |

## Incident proof

| Question | Evidence |
| --- | --- |
| What arrived? | 500 ORU-style messages in the incident report |
| What failed? | 218 terminology failures in DLQ before replay |
| Why did it fail? | Rule `ORU.OBS.CODE.MAP_REQUIRED` for `LAB:GLUCOSE_FASTING` |
| What changed? | New map version `lab_map_v2` for `LAB:GLUCOSE_FASTING` |
| What replayed? | 218 DLQ records tied to the incident |
| How was recovery verified? | 500 final observations, 0 open DLQ, 3 of 3 checks passed |

## Reproducibility

Run the demo and export the report:

```bash
make incident-demo
make replay-incident
make verify-warehouse
make export-incident-report
```

The runtime report is written under `reports/`. The committed evidence files are a small proof fixture for the public site and frontend.

## Evidence rules

1. Evidence files must not contain PHI.
2. Evidence files must use synthetic or public reference data only.
3. Counts shown on the site must come from evidence files or API responses, not hardcoded UI constants.
4. If a file is illustrative, it must say so.
5. If a claim is not backed by evidence, remove the claim.

## Next hardening step

Add JSON schema validation in CI for all evidence files.
