<section class="hero">
<p class="eyebrow">Synthetic healthcare operations platform · No PHI</p>
<h1>Pokala HealthOps</h1>
<p class="lead"><strong>Healthcare Interface Operations Platform</strong> for detecting, triaging, replaying, verifying, and auditing clinical data pipeline failures.</p>
<p><span class="pill">HL7-style ORU ingest</span><span class="pill">FHIR-oriented mapping</span><span class="pill">DLQ + replay</span><span class="pill">Warehouse verification</span><span class="pill">Audit evidence</span></p>
</section>

## Executive Snapshot

<div class="grid">
<div class="card"><div class="label">Inbound messages</div><div class="metric">500</div><p>Synthetic ORU-style lab feed.</p></div>
<div class="card"><div class="label">Detected failures</div><div class="metric">218</div><p>Terminology mapping failures routed to DLQ.</p></div>
<div class="card"><div class="label">Recovered</div><div class="metric">218</div><p>Recovered after map remediation and replay.</p></div>
<div class="card"><div class="label">Quality checks</div><div class="metric">3/3</div><p>Warehouse verification passed after replay.</p></div>
</div>

## What This Demonstrates

Pokala HealthOps demonstrates senior-level work across healthcare interoperability, backend systems, data reliability, observability, and incident response.

- Contract-driven ingestion for synthetic clinical messages
- Terminology mapping failure detection
- Dead-letter queue routing and replay
- Incident lifecycle and remediation tracking
- Warehouse quality verification
- Operational metrics and audit evidence

## Flagship Incident

The demo simulates a lab interface changing fasting glucose from GLU_FAST to LAB:GLUCOSE_FASTING. The platform detects the unmapped code, isolates failed messages, opens an incident, applies a terminology fix, replays failures, and verifies warehouse recovery.

## Run the Demo

    python -m openhip.cli incident-demo
    python -m openhip.cli replay-incident
    python -m openhip.cli verify-warehouse

## Positioning

Designed for Health IT Engineer, Interface Engineer, Interoperability Engineer, Healthcare Data Engineer, Backend Engineer, Platform Engineer, and Solutions Engineer roles.

## Guardrail

Synthetic data only. No PHI. No HIPAA certification claim. No production EHR claim.
