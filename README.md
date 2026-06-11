# Pokala HealthOps

**Healthcare Interface Operations Platform**

Live site: https://krishnasaipokala.github.io/pokala-healthops/

Pokala HealthOps is a no-PHI healthcare interface operations platform that demonstrates production-style clinical data reliability workflows.

## Flagship Incident

A lab feed changes fasting glucose from `GLU_FAST` to `LAB:GLUCOSE_FASTING`. The platform detects 218 mapping failures, routes them to DLQ, applies remediation, replays failed records, verifies recovery, and exports evidence.

## Local Demo

    python -m openhip.cli incident-demo
    python -m openhip.cli replay-incident
    python -m openhip.cli verify-warehouse

## Guardrail

Synthetic data only. No PHI. No HIPAA certification claim. No production EHR claim.
