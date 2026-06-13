# Contracts

The ORU contract is a rule source for the interface demo. It should define required fields, validation rules, mapping requirements, SLA expectations, and affected assets.

## Current behavior

The current implementation validates core required fields and rejects future observation timestamps. It also enforces terminology mapping through the pipeline.

## Required hardening

The next version should return structured validation failures:

```json
{
  "rule_id": "ORU.OBS.CODE.MAP_REQUIRED",
  "field": "observation_code",
  "category": "terminology",
  "severity": "error",
  "message": "No active mapping exists for LAB:GLUCOSE_FASTING"
}
```

## Contract rules to add

| Rule | Purpose |
| --- | --- |
| Required field | Reject incomplete messages |
| Type check | Reject invalid values before persistence |
| Date check | Reject future observation timestamps |
| Mapping required | Reject unmapped local codes |
| Active mapping required | Reject inactive maps |
| Unit allowed list | Keep observations semantically consistent |
| Contract version | Tie failures to the active rule set |

## Acceptance bar

Changing the YAML contract must change validation behavior without editing pipeline code.
