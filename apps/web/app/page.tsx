"use client";

import { useMemo, useState } from "react";

type TabKey = "overview" | "dlq" | "recovery" | "warehouse" | "audit" | "evidence";
type LayerKey = "validation" | "terminology" | "dlq" | "recovery" | "warehouse" | "audit";

const incident = {
  incident_id: "INC-TERM-MAP-001",
  title: "Terminology mapping failure recovery",
  boundary: "Synthetic no-PHI reference incident",
  inbound_messages: 500,
  accepted_initially: 282,
  terminology_failures: 218,
  recovered_messages: 218,
  open_dlq_after_recovery: 0,
  duplicate_observations: 0,
  warehouse_checks_passed: 3,
  warehouse_checks_total: 3,
  closure_status: "closed",
  closure_predicate: "(R = F) and (O = 0) and (D = 0) and (W = T)",
};

const checks = [
  ["Recovery reconciliation", "R = F", "218 = 218", "Prevents incomplete recovery of the isolated failure set."],
  ["DLQ closure", "O = 0", "0", "Prevents unresolved failed records after recovery."],
  ["Duplicate prevention", "D = 0", "0", "Prevents recovery side effects that create duplicate observations."],
  ["Warehouse verification", "W = T", "3 = 3", "Prevents unverified downstream state after remediation."],
];

const auditEvents = [
  ["01", "incident.opened", "Synthetic ORU-style terminology failure incident opened."],
  ["02", "dlq.isolated", "218 failed records preserved as recoverable objects."],
  ["03", "terminology.remediated", "Mapping condition corrected before controlled recovery."],
  ["04", "recovery.completed", "218 of 218 isolated records recovered."],
  ["05", "warehouse.verified", "3 of 3 warehouse checks passed."],
  ["06", "evidence.exported", "Closure artifacts made inspectable for review."],
];

const lifecycle = [
  ["Ingest", "500 synthetic ORU-style messages enter the pipeline."],
  ["Validate", "Terminology mapping decides accepted versus failed records."],
  ["Isolate", "218 failed records move to DLQ instead of being dropped or forced downstream."],
  ["Remediate", "Mapping condition is corrected before recovery."],
  ["Recover", "218 of 218 isolated records are processed after remediation."],
  ["Verify", "Warehouse checks pass and duplicate observations remain zero."],
  ["Close", "Closure predicate is satisfied with open DLQ at zero."],
];

const layers: Record<LayerKey, { title: string; path: string; prevents: string; proof: string }> = {
  validation: {
    title: "Interface validation",
    path: "contracts/oru_observation.yaml",
    prevents: "Bad observation-result messages entering trusted storage as if they were valid.",
    proof: "Accepted/failed split: 282 accepted initially and 218 isolated failures.",
  },
  terminology: {
    title: "Terminology mapping",
    path: "openhip/terminology.py",
    prevents: "Unmapped local codes being treated as reliable clinical semantics.",
    proof: "Reference failure mode: terminology validation failure.",
  },
  dlq: {
    title: "Dead-letter isolation",
    path: "openhip/pipeline.py",
    prevents: "Silent loss, blind retry loops, and uncontrolled downstream writes.",
    proof: "218 failed records preserved for controlled recovery.",
  },
  recovery: {
    title: "Recovery control",
    path: "openhip/cli.py",
    prevents: "Replay/recovery side effects that duplicate observations or hide partial failure.",
    proof: "Recovered records: 218 of 218, duplicate observations: 0.",
  },
  warehouse: {
    title: "Warehouse verification",
    path: "openhip/warehouse.py",
    prevents: "Declaring an incident closed before downstream state is checked.",
    proof: "Warehouse checks: 3 of 3 passed.",
  },
  audit: {
    title: "Audit and evidence export",
    path: "evidence/incident-report.json",
    prevents: "A reviewer having to trust a dashboard without inspectable proof.",
    proof: "Incident, recovery, warehouse, duplicate, and audit evidence are surfaced.",
  },
};

const runCommands = [
  "python -m openhip.cli incident-demo",
  "python -m openhip.cli replay-incident",
  "python -m openhip.cli verify-warehouse",
  "python -m openhip.cli verify-replay-invariants",
  "python -m openhip.cli export-incident-report",
];

const navItems = [
  ["console", "Console"],
  ["architecture", "Architecture"],
  ["recovery", "Recovery"],
  ["platform", "Platform"],
  ["evidence", "Evidence"],
];

const tabs: [TabKey, string][] = [
  ["overview", "Overview"],
  ["dlq", "DLQ"],
  ["recovery", "Recovery"],
  ["warehouse", "Warehouse"],
  ["audit", "Audit"],
  ["evidence", "Evidence"],
];

function jsonBlock(name: string, value: unknown) {
  return { name, content: JSON.stringify(value, null, 2) };
}

export default function Page() {
  const [tab, setTab] = useState<TabKey>("overview");
  const [layer, setLayer] = useState<LayerKey>("dlq");
  const [copied, setCopied] = useState<string>("");

  const evidenceBlocks = useMemo(
    () => [
      jsonBlock("incident-report.json", incident),
      jsonBlock("quality-checks.json", { checks }),
      jsonBlock("replay-report.json", {
        replay_attempt_id: "RPLY-TERM-MAP-001",
        incident_id: incident.incident_id,
        attempted_records: 218,
        successful_records: 218,
        failed_records: 0,
        closure_predicate: incident.closure_predicate,
      }),
      jsonBlock("audit-events.json", { events: auditEvents }),
    ],
    [],
  );

  async function copyCommand(command: string) {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(command);
      window.setTimeout(() => setCopied(""), 1400);
    } catch {
      setCopied("Copy unavailable");
      window.setTimeout(() => setCopied(""), 1400);
    }
  }

  return (
    <main className="pho-shell">
      <header className="pho-topbar" aria-label="Pokala HealthOps navigation">
        <a className="pho-brand" href="#console" aria-label="Pokala HealthOps home">
          <span className="pho-brand-dot" />
          <span>Pokala HealthOps</span>
        </a>
        <nav className="pho-nav" aria-label="Section navigation">
          {navItems.map(([href, label]) => (
            <a key={href} href={`#${href}`}>
              {label}
            </a>
          ))}
        </nav>
      </header>

      <section id="console" className="pho-hero pho-section">
        <div className="pho-hero-copy">
          <p className="pho-eyebrow">NO-PHI | HEALTHCARE RELIABILITY | PLATFORM ENGINEERING</p>
          <h1>Healthcare Interface Reliability Control Plane</h1>
          <p className="pho-lede">
            A production-shaped, local-first platform for detecting interface failures, isolating bad messages,
            recovering remediated records, verifying warehouse closure, and exporting operator evidence.
          </p>
          <div className="pho-actions">
            <a href="#evidence" className="pho-button pho-button-primary">Review evidence</a>
            <a href="#platform" className="pho-button">See platform stack</a>
          </div>
          <p className="pho-boundary">Synthetic only | no PHI | no clinical claims</p>
        </div>

        <div className="pho-console-card" aria-label="Reference incident status">
          <div className="pho-console-head">
            <div>
              <p className="pho-label">Reference incident</p>
              <h2>{incident.incident_id}</h2>
            </div>
            <span className="pho-status">CLOSED</span>
          </div>
          <div className="pho-metrics-grid">
            <Metric label="Inbound" value="500" />
            <Metric label="Failed" value="218" />
            <Metric label="Recovered" value="218" />
            <Metric label="Open DLQ" value="0" />
            <Metric label="Warehouse" value="3/3" />
            <Metric label="Duplicates" value="0" />
          </div>
          <div className="pho-proof-line">Closed iff {incident.closure_predicate}</div>
        </div>
      </section>

      <section className="pho-section pho-tabs-card" aria-label="Interactive incident console">
        <div className="pho-section-heading">
          <p className="pho-eyebrow">STATIC EVIDENCE-BACKED DASHBOARD</p>
          <h2>Incident console without a hosted backend bill</h2>
          <p>
            The public site is static, but the displayed incident is structured as an inspectable evidence bundle.
            Reviewers can inspect the same operational story they can reproduce locally from the repository.
          </p>
        </div>
        <div className="pho-tab-list" role="tablist" aria-label="Incident evidence tabs">
          {tabs.map(([key, label]) => (
            <button
              key={key}
              type="button"
              role="tab"
              aria-selected={tab === key}
              className={tab === key ? "pho-tab active" : "pho-tab"}
              onClick={() => setTab(key)}
            >
              {label}
            </button>
          ))}
        </div>
        <TabPanel tab={tab} evidenceBlocks={evidenceBlocks} />
      </section>

      <section id="architecture" className="pho-section">
        <div className="pho-section-heading">
          <p className="pho-eyebrow">ARCHITECTURE</p>
          <h2>Failure-path architecture with drilldowns</h2>
          <p>
            The artifact is not a dashboard-only demo. Each layer answers what failed, where it was isolated,
            how it was recovered, and what evidence proves closure.
          </p>
        </div>
        <div className="pho-architecture-grid">
          <div className="pho-layer-list">
            {(Object.keys(layers) as LayerKey[]).map((key) => (
              <button
                type="button"
                key={key}
                className={layer === key ? "pho-layer active" : "pho-layer"}
                onClick={() => setLayer(key)}
              >
                {layers[key].title}
              </button>
            ))}
          </div>
          <div className="pho-layer-detail">
            <p className="pho-label">Selected layer</p>
            <h3>{layers[layer].title}</h3>
            <dl>
              <div><dt>Repo path</dt><dd>{layers[layer].path}</dd></div>
              <div><dt>Prevents</dt><dd>{layers[layer].prevents}</dd></div>
              <div><dt>Proof</dt><dd>{layers[layer].proof}</dd></div>
            </dl>
          </div>
        </div>
      </section>

      <section id="recovery" className="pho-section">
        <div className="pho-section-heading">
          <p className="pho-eyebrow">RECOVERY</p>
          <h2>Replay-safe recovery lifecycle</h2>
          <p>
            Recovery is shown as a state sequence, not an informal retry. The incident closes only after count
            reconciliation, DLQ closure, duplicate prevention, and warehouse verification.
          </p>
        </div>
        <div className="pho-stepper">
          {lifecycle.map(([title, text], index) => (
            <div className="pho-step" key={title}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="platform" className="pho-section pho-platform-grid">
        <div className="pho-section-heading">
          <p className="pho-eyebrow">PLATFORM</p>
          <h2>Zero-cloud-bill by design</h2>
          <p>
            The public surface is static. The backend workflow runs locally. No hosted PHI, no paid compute,
            no GPU, and no fake live telemetry are required for the portfolio version.
          </p>
        </div>
        <div className="pho-command-card">
          <h3>Run the incident locally</h3>
          <p>Copy these commands after installing the repository development dependencies.</p>
          <div className="pho-command-list">
            {runCommands.map((command) => (
              <button key={command} type="button" onClick={() => copyCommand(command)}>
                <code>{command}</code>
              </button>
            ))}
          </div>
          <p className="pho-copy-status">{copied ? `Copied: ${copied}` : "Click a command to copy."}</p>
        </div>
        <div className="pho-proof-stack">
          <h3>Engineering proof strip</h3>
          <ul>
            <li>TypeScript typecheck</li>
            <li>Next.js static build</li>
            <li>Python ruff + mypy</li>
            <li>Behavioral tests: 18 passed</li>
            <li>MkDocs strict build</li>
            <li>GitHub Pages deploy</li>
          </ul>
        </div>
      </section>

      <section id="evidence" className="pho-section">
        <div className="pho-section-heading">
          <p className="pho-eyebrow">EVIDENCE</p>
          <h2>Closure predicate ledger</h2>
          <p>
            The incident is not closed because a command completed. It is closed because each predicate is satisfied.
          </p>
        </div>
        <div className="pho-ledger">
          {checks.map(([name, expected, observed, prevents]) => (
            <article key={name} className="pho-ledger-row">
              <div><h3>{name}</h3><p>{prevents}</p></div>
              <strong>{expected}</strong>
              <span>{observed}</span>
            </article>
          ))}
        </div>
      </section>

      <footer className="pho-footer">
        <strong>Boundary:</strong> This is a no-PHI synthetic portfolio system. It does not claim HIPAA certification,
        production EHR connectivity, clinical decision support, or real patient data processing.
      </footer>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="pho-metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function TabPanel({ tab, evidenceBlocks }: { tab: TabKey; evidenceBlocks: { name: string; content: string }[] }) {
  if (tab === "overview") {
    return (
      <div className="pho-tab-panel">
        <h3>Operational snapshot</h3>
        <p>
          500 synthetic messages were processed. 218 terminology failures were isolated, remediated, and recovered.
          The DLQ closed to zero, warehouse checks passed, and duplicate observations remained zero.
        </p>
      </div>
    );
  }
  if (tab === "dlq") {
    return (
      <div className="pho-tab-panel">
        <h3>Dead-letter queue</h3>
        <p>Failure set isolated: 218 records. Open DLQ after recovery: 0 records.</p>
      </div>
    );
  }
  if (tab === "recovery") {
    return (
      <div className="pho-tab-panel">
        <h3>Controlled recovery</h3>
        <p>Recovered records equal isolated failures: 218 of 218. Recovery is explicit, not silent retry.</p>
      </div>
    );
  }
  if (tab === "warehouse") {
    return (
      <div className="pho-tab-panel">
        <h3>Warehouse verification</h3>
        <p>Warehouse checks passed: 3 of 3. Duplicate observations: 0.</p>
      </div>
    );
  }
  if (tab === "audit") {
    return (
      <div className="pho-tab-panel pho-timeline">
        {auditEvents.map(([step, event, summary]) => (
          <div key={step}>
            <span>{step}</span>
            <strong>{event}</strong>
            <p>{summary}</p>
          </div>
        ))}
      </div>
    );
  }
  return (
    <div className="pho-tab-panel pho-evidence-list">
      {evidenceBlocks.map((block) => (
        <details key={block.name}>
          <summary>{block.name}</summary>
          <pre>{block.content}</pre>
        </details>
      ))}
    </div>
  );
}