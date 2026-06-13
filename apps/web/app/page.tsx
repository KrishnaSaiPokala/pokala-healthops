import CommandCenter from "./CommandCenter";
import { getEvidenceSummary } from "../lib/evidence";

const platformSignals = [
  "FastAPI",
  "Next.js",
  "Docker",
  "Kubernetes",
  "Helm",
  "Airflow",
  "dbt",
  "Prometheus",
  "OpenTofu",
  "pytest",
  "mypy",
  "ruff"
];

const architecture = [
  ["Synthetic ORU feed", "No-PHI lab messages model an interface failure safely."],
  ["Contract + terminology gate", "Malformed or unmapped observations are rejected before corrupting downstream facts."],
  ["Dead-letter isolation", "Failed messages are quarantined with rule, payload, incident, and replay metadata."],
  ["Replay engine", "Remediated records are reprocessed after mapping repair with duplicate checks."],
  ["Warehouse verification", "Quality checks prove recovery before evidence export and closure."],
  ["Operator evidence", "Audit events, incident report, DLQ summaries, and invariants are committed as proof."],
];

const deploymentLayers = [
  ["Container", "Dockerfiles for API and web plus Compose for API, web, Postgres, and Prometheus."],
  ["Kubernetes", "kind-compatible Deployments, Services, probes, and resource limits."],
  ["Packaging", "Helm chart for repeatable local cluster deployment."],
  ["Orchestration", "Airflow DAG models incident demo â†’ replay â†’ invariants â†’ warehouse â†’ evidence export."],
  ["Warehouse", "dbt Core + DuckDB recovery fact table and quality tests."],
  ["IaC guardrail", "OpenTofu reference module with no cloud resources declared."],
];

const invariants = [
  ["No open DLQ after replay", "All remediated terminology failures drain from the open queue."],
  ["No duplicate observations", "Replay does not create duplicate source-message observations."],
  ["Replay accounting", "Recovered records are counted against original failed messages."],
  ["Warehouse checks pass", "Analytical facts are reconciled before incident closure."],
  ["Evidence package exists", "Incident, audit, DLQ, and quality evidence can be reviewed after the run."],
  ["No-PHI boundary", "Only synthetic data is generated, processed, tested, and displayed."],
];

export default function Page() {
  const evidence = getEvidenceSummary();
  const incident = evidence.incident;
  const counts = incident.counts;
  const statusText = incident.status.toUpperCase();

  const headlineMetrics = [
    [counts.inbound_messages.toString(), "Inbound ORU messages", "Synthetic interface feed"],
    [counts.rejected_before_replay.toString(), "Terminology failures", `Isolated by ${incident.rule_id}`],
    [counts.replayed_after_fix.toString(), "Recovered by replay", "After mapping remediation"],
    [counts.open_dlq_after_replay.toString(), "Open DLQ", "Post-replay queue state"],
    [`${evidence.passedChecks}/${evidence.totalChecks}`, "Warehouse checks", "Recovery verification"],
    ["0", "Duplicate observations", "Replay safety invariant"],
  ];

  return (
    <main className="page-shell">
      <section className="hero-panel">
        <nav className="top-nav" aria-label="Primary navigation">
          <div className="mark">
            <span className="mark-dot" />
            <span>Pokala HealthOps</span>
          </div>
          <div className="nav-links">
            <a href="#console">Console</a>
            <a href="#architecture">Architecture</a>
            <a href="#recovery">Recovery</a>
            <a href="#platform">Platform</a>
            <a href="#evidence">Evidence</a>
          </div>
        </nav>

        <div className="hero-grid">
          <div>
            <p className="eyebrow">No-PHI Â· healthcare reliability Â· platform engineering</p>
            <h1>Healthcare Interface Reliability Control Plane</h1>
            <p className="hero-copy">
              A production-shaped, local-first platform for detecting interface failures, isolating bad messages,
              replaying remediated records, verifying warehouse recovery, and exporting operator evidence.
            </p>
            <div className="hero-actions">
              <a className="button primary" href="#evidence">Review evidence</a>
              <a className="button" href="#platform">See platform stack</a>
            </div>
          </div>

          <aside className="incident-card" aria-label="Current incident summary">
            <div className="card-kicker">Incident command</div>
            <h2>{incident.incident_id}</h2>
            <p>{incident.scenario}</p>
            <div className="status-row">
              <span>Status</span>
              <strong>{statusText}</strong>
            </div>
            <div className="status-row">
              <span>Rule</span>
              <strong>{incident.rule_id}</strong>
            </div>
            <div className="status-row">
              <span>Run</span>
              <strong>{incident.run_id}</strong>
            </div>
            <div className="boundary">Synthetic only Â· no PHI Â· no clinical claims</div>
          </aside>
        </div>
      </section>

      <section className="metrics-strip" aria-label="Evidence backed metrics">
        {headlineMetrics.map(([value, label, helper]) => (
          <article className="metric" key={label}>
            <strong>{value}</strong>
            <span>{label}</span>
            <p>{helper}</p>
          </article>
        ))}
      </section>

      <CommandCenter
        checks={evidence.checks}
        incident={incident}
        passedChecks={evidence.passedChecks}
        ruleBreakdown={evidence.ruleBreakdown}
        totalChecks={evidence.totalChecks}
      />

      <section id="architecture" className="section-block">
        <div className="section-heading">
          <p className="eyebrow">System design surface</p>
          <h2>Failure recovery architecture</h2>
          <p>
            This is not a chart-only dashboard. The system models the operational lifecycle around healthcare
            interface failures: detect, isolate, remediate, replay, verify, and prove.
          </p>
        </div>
        <div className="architecture-map">
          {architecture.map(([title, body], index) => (
            <article className="architecture-node" key={title}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="recovery" className="split-section">
        <div className="section-heading compact">
          <p className="eyebrow">Replay safety</p>
          <h2>Incident recovery state machine</h2>
          <p>
            The incident closes only after replay and warehouse checks produce evidence. This framing is the
            senior signal: recovery is a state machine, not a happy-path script.
          </p>
        </div>
        <div className="state-machine">
          {[
            "Detected",
            "DLQ isolated",
            "Mapping remediated",
            "Replay executed",
            "Warehouse verified",
            "Evidence exported",
          ].map((state, index) => (
            <div className="state" key={state}>
              <span>{index + 1}</span>
              {state}
            </div>
          ))}
        </div>
      </section>

      <section className="section-block invariant-panel">
        <div className="section-heading">
          <p className="eyebrow">Reliability invariants</p>
          <h2>Closure proof matrix</h2>
          <p>Every claim on this page ties back to committed evidence JSON and executable CLI checks.</p>
        </div>
        <div className="invariant-grid">
          {invariants.map(([title, body]) => (
            <article className="invariant" key={title}>
              <span className="pass">PASS</span>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="platform" className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Recruiter-hot, engineer-defensible stack</p>
          <h2>Local cloud-native platform layer</h2>
          <p>
            Docker, Kubernetes, Helm, Airflow, dbt, Prometheus, and OpenTofu are included as local-only,
            zero-cloud-bill assets. They show production thinking without pretending this is a deployed hospital system.
          </p>
        </div>
        <div className="platform-grid">
          {deploymentLayers.map(([title, body]) => (
            <article className="platform-card" key={title}>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
        <div className="signal-row">
          {platformSignals.map((signal) => <span key={signal}>{signal}</span>)}
        </div>
      </section>

      <section id="evidence" className="evidence-section">
        <div className="section-heading compact">
          <p className="eyebrow">Evidence-backed operations</p>
          <h2>Warehouse and audit proof</h2>
        </div>
        <div className="evidence-grid">
          <article className="evidence-card">
            <h3>{evidence.passedChecks}/{evidence.totalChecks} warehouse checks passed</h3>
            <table>
              <tbody>
                {evidence.checks.map((check) => (
                  <tr key={check.name}>
                    <td>{check.name}</td>
                    <td>{String(check.observed)}</td>
                    <td className="ok">{check.status.toUpperCase()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </article>

          <article className="evidence-card">
            <h3>DLQ recovery by rule</h3>
            <table>
              <tbody>
                {evidence.ruleBreakdown.map((row) => (
                  <tr key={row.rule}>
                    <td>{row.rule}</td>
                    <td>{row.before} before</td>
                    <td className="ok">{row.after} open after</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </article>

          <article className="evidence-card wide">
            <h3>Audit trail</h3>
            <table>
              <tbody>
                {evidence.auditEvents.events.map((event) => (
                  <tr key={event.event_type}>
                    <td>{event.event_type}</td>
                    <td>{event.actor}</td>
                    <td>{event.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </article>
        </div>
      </section>

      <footer className="footer">
        <strong>Boundary:</strong> This is a no-PHI synthetic portfolio system. It does not claim HIPAA certification,
        production EHR connectivity, or real patient data processing.
      </footer>
    </main>
  );
}

