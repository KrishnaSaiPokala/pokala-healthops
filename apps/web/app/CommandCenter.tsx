"use client";

import { useMemo, useState } from "react";

type IncidentCounts = {
  inbound_messages: number;
  rejected_before_replay: number;
  replayed_after_fix: number;
  open_dlq_after_replay: number;
};

type Incident = {
  incident_id: string;
  scenario: string;
  status: string;
  rule_id: string;
  run_id: string;
  counts: IncidentCounts;
};

type Check = {
  name: string;
  observed: string | number | boolean;
  status: string;
};

type RuleBreakdown = {
  rule: string;
  before: number;
  after: number;
};

type CommandCenterProps = {
  incident: Incident;
  checks: Check[];
  passedChecks: number;
  ruleBreakdown: RuleBreakdown[];
  totalChecks: number;
};

type TabId = "incident" | "dlq" | "replay" | "evidence";

const tabs: Array<{ id: TabId; label: string; helper: string }> = [
  { id: "incident", label: "Incident", helper: "command triage" },
  { id: "dlq", label: "DLQ", helper: "quarantine view" },
  { id: "replay", label: "Replay", helper: "safe recovery" },
  { id: "evidence", label: "Evidence", helper: "closure proof" },
];

const timeline = [
  "Detected",
  "DLQ isolated",
  "Mapping remediated",
  "Replay executed",
  "Warehouse verified",
  "Evidence exported",
];

export default function CommandCenter({
  checks,
  incident,
  passedChecks,
  ruleBreakdown,
  totalChecks,
}: CommandCenterProps) {
  const [active, setActive] = useState<TabId>("incident");

  const failedBefore = ruleBreakdown.reduce((sum, row) => sum + row.before, 0);
  const openAfter = ruleBreakdown.reduce((sum, row) => sum + row.after, 0);

  const activePanel = useMemo(() => {
    switch (active) {
      case "dlq":
        return {
          title: "Dead-letter queue isolation",
          command: "healthops dlq summary --incident latest",
          summary:
            "Terminology failures are quarantined before they can pollute observation facts or downstream warehouse checks.",
          output: [
            `rule=${incident.rule_id}`,
            `failed_before_replay=${failedBefore}`,
            `open_after_replay=${openAfter}`,
            "quarantine_status=drained",
          ],
        };
      case "replay":
        return {
          title: "Deterministic replay execution",
          command: "healthops replay --after-remediation --verify-invariants",
          summary:
            "Replay only closes the incident after recovered records match the original failure count and duplicate source checks pass.",
          output: [
            `replayed_records=${incident.counts.replayed_after_fix}`,
            `open_dlq=${incident.counts.open_dlq_after_replay}`,
            "duplicate_observations=0",
            "replay_mode=idempotent",
          ],
        };
      case "evidence":
        return {
          title: "Evidence package export",
          command: "healthops evidence export --format json",
          summary:
            "Closure proof is packaged as incident, DLQ, replay, audit, and warehouse evidence rather than a screenshot-only claim.",
          output: [
            `warehouse_checks=${passedChecks}/${totalChecks}`,
            `incident_status=${incident.status}`,
            "evidence_format=json",
            "boundary=no_phi_synthetic_only",
          ],
        };
      default:
        return {
          title: "Incident command overview",
          command: "healthops incident demo --scenario terminology-outage",
          summary:
            "A synthetic ORU terminology outage is detected, isolated, remediated, replayed, verified, and closed with evidence.",
          output: [
            `incident=${incident.incident_id}`,
            `run=${incident.run_id}`,
            `status=${incident.status}`,
            `scenario="${incident.scenario}"`,
          ],
        };
    }
  }, [active, failedBefore, incident, openAfter, passedChecks, totalChecks]);

  return (
    <section id="console" className="command-center section-block">
      <div className="section-heading">
        <p className="eyebrow">Interactive platform demo</p>
        <h2>Operator command center</h2>
        <p>
          Switch between incident, DLQ, replay, and evidence views. This turns the case study into a
          product-style operations surface while still keeping every number tied to synthetic committed evidence.
        </p>
      </div>

      <div className="console-shell">
        <div className="console-tabs" role="tablist" aria-label="Command center views">
          {tabs.map((tab) => (
            <button
              aria-selected={active === tab.id}
              className={active === tab.id ? "console-tab active" : "console-tab"}
              key={tab.id}
              onClick={() => setActive(tab.id)}
              role="tab"
              type="button"
            >
              <span>{tab.label}</span>
              <small>{tab.helper}</small>
            </button>
          ))}
        </div>

        <div className="console-grid">
          <article className="terminal-panel">
            <div className="terminal-chrome">
              <span />
              <span />
              <span />
              <strong>{activePanel.title}</strong>
            </div>
            <div className="terminal-command">$ {activePanel.command}</div>
            <p>{activePanel.summary}</p>
            <div className="terminal-output" aria-label="Command output">
              {activePanel.output.map((line) => (
                <code key={line}>{line}</code>
              ))}
            </div>
          </article>

          <article className="replay-timeline-card">
            <div className="mini-heading">
              <span>Replay timeline</span>
              <strong>{incident.status.toUpperCase()}</strong>
            </div>
            <ol className="replay-timeline">
              {timeline.map((item, index) => (
                <li key={item}>
                  <span>{index + 1}</span>
                  <p>{item}</p>
                  <strong>complete</strong>
                </li>
              ))}
            </ol>
          </article>
        </div>

        <div className="evidence-drawers">
          <details open>
            <summary>Incident evidence snapshot</summary>
            <pre>{`{
  "incident_id": "${incident.incident_id}",
  "rule_id": "${incident.rule_id}",
  "status": "${incident.status}",
  "replayed_after_fix": ${incident.counts.replayed_after_fix},
  "open_dlq_after_replay": ${incident.counts.open_dlq_after_replay}
}`}</pre>
          </details>

          <details>
            <summary>Warehouse check sample</summary>
            <pre>{`{
  "passed": ${passedChecks},
  "total": ${totalChecks},
  "checks": [
${checks
  .slice(0, 3)
  .map((check) => `    { "name": "${check.name}", "observed": "${String(check.observed)}", "status": "${check.status}" }`)
  .join(",\n")}
  ]
}`}</pre>
          </details>

          <details>
            <summary>DLQ rule recovery</summary>
            <pre>{`{
${ruleBreakdown
  .map((row) => `  "${row.rule}": { "before": ${row.before}, "open_after": ${row.after} }`)
  .join(",\n")}
}`}</pre>
          </details>
        </div>

        <div className="operator-ctas">
          <a href="https://github.com/KrishnaSaiPokala/pokala-healthops">View repository</a>
          <a href="https://github.com/KrishnaSaiPokala/pokala-healthops/tree/main/docs">Read technical docs</a>
          <a href="https://github.com/KrishnaSaiPokala/pokala-healthops#readme">Run locally</a>
        </div>
      </div>
    </section>
  );
}
