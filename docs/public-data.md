# Public-reference data

The core incident remains synthetic because the demo needs a controlled, repeatable interface failure. Public datasets are used only as reference context.

## Current sample

The repository includes a small provider-reference sample:

```text
data/public/provider_reference_sample.csv
```

The sample contains synthetic provider identifiers used by the ORU feed, including `PRAC-0001`. The enrichment code lives in:

```text
openhip/public_data.py
```

## Why this matters

Public-reference enrichment keeps the demo safe while making the operational model more realistic. A lab interface usually carries provider or facility identifiers. A command center should be able to attach context such as specialty, state, source facility, or reference-data provenance.

## Boundaries

The project does not ingest PHI. It does not use real patient records. Public-reference data must remain non-patient-level and must be documented before use.

## Next increments

- facility-reference sample
- source-interface region mapping
- provider specialty distribution in the dashboard
- evidence file for reference-data enrichment
