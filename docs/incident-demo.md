# Incident walkthrough

1. **Ingest.** 500 ORU messages arrive on `lab_oru_feed`. The first 218 use the
   new `LAB:GLUCOSE_FASTING` code.
2. **Validate.** Each message is checked against `oru_contract.yml`: required
   fields present, timestamp not in the future.
3. **Map.** The new code has no active entry, so 218 messages fail
   `ORU.OBS.CODE.MAP_REQUIRED` and go to the dead-letter queue. An incident
   opens automatically.
4. **Remediate.** An analyst adds the `LAB:GLUCOSE_FASTING` map (version
   `lab_map_v2`).
5. **Replay.** The 218 dead-lettered payloads are reprocessed through the same
   pipeline. All 218 are accepted.
6. **Verify.** Three checks confirm observations exist, no dead-letters remain
   open, and the incident is marked remediated.
7. **Report.** `reports/INC-20260602-LAB-CODE-FORMAT.json` is the evidence
   artifact, including before/after counts.

Replay is explicit and audited. There is no silent retry of domain failures.
