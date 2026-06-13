# Implemented versus roadmap

The project stays credible by separating what runs from what is planned.

## Runs today

1. Synthetic lab incident generation.
2. Contract validation from YAML.
3. Terminology mapping failure to DLQ.
4. Incident creation.
5. Map remediation.
6. Replay through the same pipeline.
7. Warehouse verification.
8. JSON incident report export.
9. API inspection endpoints.
10. MkDocs public site.
11. CI quality gate for Python, tests, demo, replay, verification, and docs.

## Needs hardening before stronger claims

1. Dashboard must read live API state or committed evidence JSON.
2. Evidence files must be committed or generated and validated in CI.
3. Replay must prove idempotency and partial failure behavior.
4. Contract engine must enforce more than required fields.
5. Metrics must expose operational labels, counters, and histograms.
6. Security must include threat model and free scans.
7. Public reference enrichment must be added before calling the data layer realistic.

## Future work

1. Public provider and facility reference enrichment.
2. Browser-side command center backed by evidence JSON.
3. Rule-based incident analyst with no paid API and no PHI upload.
4. FHIR hardening or clear experimental labeling.
5. dbt-lite warehouse if it compiles and tests in CI.
6. Better audit timeline and replay-attempt model.
