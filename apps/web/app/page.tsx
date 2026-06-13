import { getEvidenceSummary } from "../lib/evidence";

export default function Page() {
  const evidence = getEvidenceSummary();
  const incident = evidence.incident;
  const statusText = incident.status.toUpperCase();

  return (
    <main className="shell">
      <aside className="rail">
        <div className="brand">Pokala<br />HealthOps</div>
        <div className="rail-sub">Interface reliability demo</div>
        <nav className="nav">
          <a className="active" href="#command">Command Center</a>
          <a href="#incident">Incident</a>
          <a href="#dlq">DLQ</a>
          <a href="#warehouse">Verification</a>
          <a href="#audit">Audit</a>
        </nav>
        <div className="no-phi">Synthetic data only. No PHI. No clinical claims.</div>
      </aside>

      <section className="workspace">
        <header id="command" className="topbar">
          <div>
            <p className="eyebrow">Evidence backed · local first · no PHI</p>
            <h1>InterfaceOps Command Center</h1>
            <p className="lead">
              Detect, triage, replay, verify, and audit one controlled healthcare interface failure.
              Counts on this page come from committed evidence JSON, not inline UI constants.
            </p>
          </div>
          <div className="health">INCIDENT: {statusText}</div>
        </header>

        <section className="grid4">
          {evidence.metrics.map((metric) => (
            <div className={`card metric-card ${metric.tone}`} key={metric.label}>
              <div className="label">{metric.label}</div>
              <div className="value">{metric.value}</div>
              <p>{metric.helper}</p>
            </div>
          ))}
        </section>

        <section id="incident" className="grid2">
          <div className="card">
            <div className="label">Incident</div>
            <h2>{incident.incident_id}</h2>
            <p>{incident.scenario}</p>
            <span className="pill">Rule: {incident.rule_id}</span>
            <span className="pill">Status: {incident.status}</span>
            <span className="pill">Run: {incident.run_id}</span>
            <span className="pill">Policy: no PHI</span>
          </div>

          <div className="card timeline">
            <div className="step"><strong>Detect</strong><br />{incident.counts.rejected_before_replay} records failed the mapping rule.</div>
            <div className="step"><strong>Remediate</strong><br />Map version {incident.remediation.new_mapping_version} added {incident.remediation.source_code}.</div>
            <div className="step"><strong>Replay</strong><br />{incident.counts.replayed_after_fix} records recovered through replay.</div>
            <div className="step"><strong>Verify</strong><br />{evidence.passedChecks}/{evidence.totalChecks} warehouse checks passed.</div>
          </div>
        </section>

        <section id="dlq" className="card">
          <div className="label">Dead Letter Queue</div>
          <h2>Failure Queue Recovery</h2>
          <table>
            <thead>
              <tr><th>Rule</th><th>Before replay</th><th>After replay</th><th>Outcome</th></tr>
            </thead>
            <tbody>
              {evidence.ruleBreakdown.map((row) => (
                <tr key={row.rule}>
                  <td>{row.rule}</td>
                  <td>{row.before} open</td>
                  <td>{row.after} open</td>
                  <td className="ok">{row.after === 0 ? "Recovered" : "Open"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section id="warehouse" className="grid2">
          <div className="card">
            <div className="label">Warehouse Verification</div>
            <h2>{evidence.passedChecks}/{evidence.totalChecks} Checks Passed</h2>
            <table>
              <tbody>
                {evidence.checks.map((check) => (
                  <tr key={check.name}>
                    <td>{check.name}</td>
                    <td className="ok">{check.status.toUpperCase()}</td>
                    <td>{String(check.observed)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div id="audit" className="card">
            <div className="label">Audit Evidence</div>
            <h2>Operational Events</h2>
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
          </div>
        </section>
      </section>
    </main>
  );
}
