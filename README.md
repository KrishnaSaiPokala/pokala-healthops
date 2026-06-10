# OpenHIP Command Center

A local-first, no-PHI EHR InterfaceOps platform for HL7/FHIR ingestion,
data contracts, dead-letter replay, terminology mapping, MPI demonstration,
observability, audit logging, and analytics-ready healthcare pipelines.

## No-PHI Guardrail

This project uses only synthetic/demo data. Do not upload, paste, ingest,
commit, or process real patient data, employer data, credentials, or secrets.

## Fast Start

```bash
make bootstrap
make incident-demo
make replay-incident
make verify-warehouse
make export-incident-report
make docs
```

## Full Local Stack

```bash
make up
```

Services:

- API: http://localhost:8000/docs
- Web UI: http://localhost:3000
- HAPI FHIR: http://localhost:8080/fhir
- Grafana: http://localhost:3001
- Keycloak: http://localhost:8083
- Docs: http://localhost:8001

## Demo Story

Lab ORU feed changes observation code format from `GLU_FAST` to
`LAB:GLUCOSE_FASTING`. OpenHIP detects terminology mapping failure,
routes failed messages to DLQ, opens an incident, applies a mapping fix,
replays failed records, verifies warehouse checks, and exports evidence.

## Core Commands

```bash
make demo
make incident-demo
make replay-incident
make verify-warehouse
make export-incident-report
make test
make lint
make docs
```


## Windows / PyCharm Terminal Workflow

    cd C:\Users\Event\PycharmProjects\HAPI-FHOR-KSP\openhip-command-center
    .\scripts\windows_smoke.ps1

## Public Documentation Target

    https://KrishnaSaiPokala.github.io/openhip-command-center/

## Current Verified Core Flow

- Synthetic ORU ingestion
- Terminology mapping failure
- DLQ creation
- Incident creation
- Mapping remediation
- DLQ replay
- Warehouse-quality verification
- Incident evidence export
- MkDocs documentation build
