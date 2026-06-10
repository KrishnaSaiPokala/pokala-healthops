# Interview notes

**One line.** A no-PHI control plane that detects, triages, replays, and proves
recovery of a healthcare interface incident.

**Why it is not a dashboard.** The unit of work is the integration run. Every
number ties to a `run_id`; every failure is a managed item with a rule ID, not
a swallowed exception.

**The story.** A lab code format changes; 218 results stop loading; the contract
catches it; the analyst fixes the map; replay recovers everything; checks prove
it. That is the day-to-day of interface operations.

**What I would harden for production.** Enforce RBAC at the API, move from
SQLite to Postgres, run dbt and Great Expectations for real, and put the
terminology map behind change review.
