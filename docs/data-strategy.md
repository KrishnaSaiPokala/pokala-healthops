# Data strategy

## Position

The project is synthetic-first and public-reference-enriched.

Synthetic data powers the controlled interface incident. Public reference samples add realistic operational context without PHI.

## Why synthetic data stays in the core

The flagship incident requires exact, repeatable failure counts and replay behavior. Public datasets do not usually provide broken ORU interface messages, DLQ state, replay attempts, trace IDs, or terminology-remediation workflows.

Synthetic messages make the reliability proof deterministic.

## Where public data belongs

Public data should enrich the demo, not replace the incident engine.

Good use cases:

1. Provider reference sample.
2. Facility reference sample.
3. State or region context.
4. Public terminology examples.
5. Aggregate public health context.

Bad use cases:

1. Patient-level public claims.
2. Large uncontrolled data dumps in the repo.
3. Anything that looks like real patient data.
4. Anything with unclear license or provenance.

## Storage rule

Commit small samples. Provide scripts for larger downloads only if they are optional and documented.

## Next step

Add a small provider reference sample and use it to enrich `ordering_provider_id` in the demo warehouse and dashboard.
