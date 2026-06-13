# Evidence package

This directory contains small committed evidence fixtures for the public site and frontend.

The runtime CLI writes generated reports under `reports/`. The committed files here are stable proof fixtures that keep the site honest and inspectable.

Files:

- `incident-report.json`
- `dlq-before.json`
- `dlq-after.json`
- `quality-checks.json`
- `audit-events.json`
- `metrics-sample.prom`

Rules:

1. Synthetic data only.
2. No PHI.
3. No employer data.
4. Counts shown in the public dashboard should come from these files or API state.
