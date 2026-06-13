import { getEvidenceSummary } from "../lib/evidence";

export default function Page() {
  const evidence = getEvidenceSummary();
  const incident = evidence.incident;
  const counts = incident.counts;
  const statusText = incident.status.toUpperCase();

  const proofCards = [
    {
      label: "Inbound lab messages",
      value: counts.inbound_messages.toString(),
      detail: "Synthetic ORU feed processed through the incident path",
      tone: "blue"
    },
    {
      label: "Terminology failures",
      value: counts.rejected_before_replay.toString(),
      detail: `Rejected by ${incident.rule_id}`,
      tone: "red"
    },
    {
      label: "Recovered by replay",
      value: counts.replayed_after_fix.toString(),
      detail: "Remediated after controlled map update",
      tone: "green"
    },
    {
      label: "Open DLQ after recovery",
      value: counts.open_dlq_after_replay.toString(),
      detail: "Verified post-replay operating state",
      tone: "green"
    }
  ];

  const systemSignals = [
    "No-PHI synthetic healthcare operations system",
    "Dead-letter triage for interface failures",
    "Deterministic replay after remediation",
    "Warehouse verification after recovery",
    "Evidence export for incident review",
    "Audit trail for operational actions"
  ];

  return (
    <main className="case-shell">
      <section className="hero">
        <div className="hero-copy">
          <div className="kicker">No-PHI · Healthcare operations · Reliability engineering</div>
          <h1>Healthcare Interface Reliability Control Plane</h1>
          <p className="hero-lead">
            A synthetic health-ops command center that detects lab interface failures,
            routes bad messages into a dead-letter queue, applies remediation, replays
            recoverable records, verifies warehouse recovery, and exports incident evidence.
          </p>

          <div className="hero-actions">
            <a href="#evidence">Evidence package</a>
            <a href="#recovery">Recovery flow</a>
            <a href="#boundaries">System boundary</a>
          </div>
        </div>

        <div className="hero-panel">
          <div className="panel-label">Current incident state</div>
          <div className="incident-status">{statusText}</div>
          <div className="incident-id">{incident.incident_id}</div>
          <div className="status-grid">
            <div>
              <span>Run</span>
              <strong>{incident.run_id}</strong>
            </div>
            <div>
              <span>Rule</span>
              <strong>{incident.rule_id}</strong>
            </div>
            <div>
              <span>Policy</span>
              <strong>No PHI</strong>
            </div>
            <div>
              <span>Checks</span>
              <strong>{evidence.passedChecks}/{evidence.totalChecks} passed</strong>
            </div>
          </div>
        </div>
      </section>

      <section id="evidence" className="proof-grid">
        {proofCards.map((card) => (
          <article className={`proof-card ${card.tone}`} key={card.label}>
            <span>{card.label}</span>
            <strong>{card.value}</strong>
            <p>{card.detail}</p>
          </article>
        ))}
      </section>

      <section className="two-column">
        <article className="card narrative-card">
          <div className="section-label">What this proves</div>
          <h2>Operational recovery, not a static dashboard</h2>
          <p>
            This project is structured around an interface incident: failed terminology mapping,
            DLQ isolation, remediation, replay, warehouse reconciliation, and evidence export.
            The UI reads committed evidence JSON instead of hardcoded marketing numbers.
          </p>

          <div className="signal-list">
            {systemSignals.map((signal) => (
              <div className="signal" key={signal}>{signal}</div>
            ))}
          </div>
        </article>

        <article id="recovery" className="card recovery-card">
          <div className="section-label">Recovery path</div>
          <h2>Detect ? Remediate ? Replay ? Verify ? Evidence</h2>

          <div className="recovery-step">
            <b>01 Detect</b>
            <p>{counts.rejected_before_replay} records fail terminology contract enforcement.</p>
          </div>
          <div className="recovery-step">
            <b>02 Remediate</b>
            <p>
              Map version {incident.remediation.new_mapping_version} adds{" "}
              {incident.remediation.source_code}.
            </p>
          </div>
          <div className="recovery-step">
            <b>03 Replay</b>
            <p>{counts.replayed_after_fix} DLQ records recover through controlled replay.</p>
          </div>
          <div className="recovery-step">
            <b>04 Verify</b>
            <p>{evidence.passedChecks}/{evidence.totalChecks} warehouse checks pass after recovery.</p>
          </div>
        </article>
      </section>

      <section className="two-column">
        <article className="card">
          <div className="section-label">Dead-letter queue recovery</div>
          <h2>Failure queue drained after remediation</h2>
          <table>
            <thead>
              <tr>
                <th>Rule</th>
                <th>Before</th>
                <th>After</th>
                <th>Result</th>
              </tr>
            </thead>
            <tbody>
              {evidence.ruleBreakdown.map((row) => (
                <tr key={row.rule}>
                  <td>{row.rule}</td>
                  <td>{row.before} open</td>
                  <td>{row.after} open</td>
                  <td className={row.after === 0 ? "ok" : "fail"}>
                    {row.after === 0 ? "Recovered" : "Open"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>

        <article className="card">
          <div className="section-label">Warehouse reconciliation</div>
          <h2>Post-replay quality checks</h2>
          <table>
            <thead>
              <tr>
                <th>Check</th>
                <th>Status</th>
                <th>Observed</th>
              </tr>
            </thead>
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
        </article>
      </section>

      <section id="boundaries" className="boundary-grid">
        <article className="card boundary implemented">
          <div className="section-label">Implemented</div>
          <h2>Reliable demo system</h2>
          <ul>
            <li>Synthetic ORU ingestion path</li>
            <li>Contract and terminology validation</li>
            <li>DLQ isolation and replay</li>
            <li>Incident evidence export</li>
            <li>Warehouse verification checks</li>
            <li>Audit event capture</li>
          </ul>
        </article>

        <article className="card boundary">
          <div className="section-label">Explicitly not claimed</div>
          <h2>Clean boundaries</h2>
          <ul>
            <li>No real patient data</li>
            <li>No PHI handling claim</li>
            <li>No HIPAA certification claim</li>
            <li>No production EHR integration claim</li>
            <li>No clinical decision support claim</li>
            <li>No live hospital deployment claim</li>
          </ul>
        </article>
      </section>

      <section className="card audit-card">
        <div className="section-label">Audit evidence</div>
        <h2>Operational trail</h2>
        <table>
          <thead>
            <tr>
              <th>Event</th>
              <th>Actor</th>
              <th>Detail</th>
            </tr>
          </thead>
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
      </section>
    </main>
  );
}
