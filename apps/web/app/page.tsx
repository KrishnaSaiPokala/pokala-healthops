const metrics = [
  { label: "Inbound ORU messages", value: "500", tone: "blue", helper: "Synthetic lab feed processed." },
  { label: "Mapping failures", value: "218", tone: "red", helper: "Routed to DLQ by rule." },
  { label: "Recovered by replay", value: "218", tone: "green", helper: "Accepted after terminology fix." },
  { label: "Open DLQ", value: "0", tone: "green", helper: "Post-remediation state." }
];

const dlqRows = [
  { category: "Terminology mapping", rule: "ORU.OBS.CODE.MAP_REQUIRED", before: "218 open", after: "0 open", outcome: "Recovered" },
  { category: "Contract schema", rule: "Required fields", before: "0 open", after: "0 open", outcome: "Clean" },
  { category: "MPI reference", rule: "MRN resolves", before: "0 open", after: "0 open", outcome: "Clean" }
];

const checks = [
  { name: "fact_observation_has_rows", result: "PASS", detail: "observations=500" },
  { name: "open_deadletters_zero_after_replay", result: "PASS", detail: "open_dlq=0" },
  { name: "incident_remediated", result: "PASS", detail: "status=remediated" }
];

export default function Page() {
  return (
    <main className="shell">
      <aside className="rail">
        <div className="brand">Pokala<br />HealthOps</div>
        <div className="rail-sub">Healthcare Interface Operations Platform</div>
        <nav className="nav">
          <a className="active" href="#command">Command Center</a>
          <a href="#incident">Incident Workbench</a>
          <a href="#dlq">Dead Letter Queue</a>
          <a href="#warehouse">Warehouse Verification</a>
          <a href="#audit">Audit Evidence</a>
        </nav>
        <div className="no-phi">Synthetic data only. No PHI. No production clinical claims.</div>
      </aside>

      <section className="workspace">
        <header id="command" className="topbar">
          <div>
            <p className="eyebrow">Synthetic Healthcare Operations · No PHI</p>
            <h1>InterfaceOps Command Center</h1>
            <p className="lead">Detect, triage, replay, verify, and audit clinical data pipeline failures with production-style recovery evidence.</p>
          </div>
          <div className="health">SYSTEM HEALTH: RECOVERED</div>
        </header>

        <section className="grid4">
          {metrics.map((metric) => (
            <div className={"card metric-card " + metric.tone} key={metric.label}>
              <div className="label">{metric.label}</div>
              <div className="value">{metric.value}</div>
              <p>{metric.helper}</p>
            </div>
          ))}
        </section>

        <section id="incident" className="grid2">
          <div className="card">
            <div className="label">Active Incident</div>
            <h2>LAB-CODE-FORMAT</h2>
            <p>Source lab changed fasting glucose from <code>GLU_FAST</code> to <code>LAB:GLUCOSE_FASTING</code>. The platform detected the unmapped code, isolated affected records, remediated the terminology map, replayed failures, and verified warehouse recovery.</p>
            <span className="pill">Severity: Medium</span>
            <span className="pill">Rule: ORU.OBS.CODE.MAP_REQUIRED</span>
            <span className="pill">Status: Remediated</span>
            <span className="pill">Traceable Audit Events</span>
          </div>

          <div className="card timeline">
            <div className="step"><strong>Detect</strong><br />Reject rate breached due to terminology mapping failures.</div>
            <div className="step"><strong>Triage</strong><br />DLQ grouped 218 records under one failed rule.</div>
            <div className="step"><strong>Remediate</strong><br />New lab code was added to terminology mapping.</div>
            <div className="step"><strong>Replay</strong><br />All failed records were replayed and recovered.</div>
          </div>
        </section>

        <section id="dlq" className="card">
          <div className="label">Dead Letter Queue</div>
          <h2>Failure Queue Recovery</h2>
          <table>
            <thead>
              <tr><th>Category</th><th>Rule</th><th>Before</th><th>After Replay</th><th>Outcome</th></tr>
            </thead>
            <tbody>
              {dlqRows.map((row) => (
                <tr key={row.rule}>
                  <td>{row.category}</td>
                  <td>{row.rule}</td>
                  <td>{row.before}</td>
                  <td>{row.after}</td>
                  <td className="ok">{row.outcome}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section id="warehouse" className="grid2">
          <div className="card">
            <div className="label">Warehouse Verification</div>
            <h2>3/3 Quality Checks Passed</h2>
            <table>
              <tbody>
                {checks.map((check) => (
                  <tr key={check.name}>
                    <td>{check.name}</td>
                    <td className="ok">{check.result}</td>
                    <td>{check.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div id="audit" className="card">
            <div className="label">Audit Evidence</div>
            <h2>Operational Proof</h2>
            <p>The repo backs this dashboard with CLI workflows, API endpoints, tests, replay logic, quality checks, metrics, and incident report export.</p>
            <span className="pill">Incident opened</span>
            <span className="pill">Replay completed</span>
            <span className="pill">Warehouse verified</span>
            <span className="pill">No PHI marker</span>
          </div>
        </section>
      </section>
    </main>
  );
}
