<div class="app-shell">
  <aside class="rail">
    <div class="brand">Pokala<br/>HealthOps</div>
    <small>Healthcare Interface Operations Platform</small>
    <a class="navitem active" href="#command">Command Center</a>
    <a class="navitem" href="#incident">Incident Workbench</a>
    <a class="navitem" href="#dlq">Dead Letter Queue</a>
    <a class="navitem" href="#warehouse">Warehouse Verification</a>
    <a class="navitem" href="#evidence">Evidence</a>
    <a class="navitem" href="https://github.com/KrishnaSaiPokala/pokala-healthops">GitHub Repo</a>
  </aside>
  <main class="main-app">
    <section id="command" class="topbar">
      <div>
        <p class="eyebrow">Synthetic healthcare operations · no PHI</p>
        <h1 class="title">InterfaceOps Command Center</h1>
        <p class="subtitle">Detect, triage, replay, verify, and audit clinical data pipeline failures with production-style recovery evidence.</p>
      </div>
      <div class="status-pill">SYSTEM HEALTH: RECOVERED</div>
    </section>
    <section class="grid">
      <div class="card"><div class="label">Inbound ORU messages</div><div class="metric blue">500</div><p>Synthetic lab feed volume.</p></div>
      <div class="card"><div class="label">Mapping failures</div><div class="metric bad">218</div><p>Routed to DLQ by rule.</p></div>
      <div class="card"><div class="label">Recovered by replay</div><div class="metric good">218</div><p>Accepted after terminology fix.</p></div>
      <div class="card"><div class="label">Open DLQ</div><div class="metric good">0</div><p>Post-remediation state.</p></div>
    </section>
    <section id="incident" class="grid-2">
      <div class="card">
        <div class="label">Active incident</div>
        <h2>LAB-CODE-FORMAT</h2>
        <p>Source lab changed fasting glucose from <code>GLU_FAST</code> to <code>LAB:GLUCOSE_FASTING</code>. The platform detected the unmapped code, isolated affected records, remediated the terminology map, replayed failures, and verified warehouse recovery.</p>
        <span class="pill">Severity: Medium</span><span class="pill">Rule: ORU.OBS.CODE.MAP_REQUIRED</span><span class="pill">Status: Remediated</span>
      </div>
      <div class="card timeline">
        <div class="step"><strong>Detect</strong><br/>Reject rate breached due to terminology mapping failures.</div>
        <div class="step"><strong>Triage</strong><br/>DLQ grouped 218 failures under one mapping rule.</div>
        <div class="step"><strong>Replay</strong><br/>Remediation recovered all failed records.</div>
      </div>
    </section>
    <section id="dlq" class="card">
      <div class="label">Dead Letter Queue</div>
      <table class="table"><thead><tr><th>Category</th><th>Rule</th><th>Before</th><th>After Replay</th><th>Outcome</th></tr></thead><tbody><tr><td>Terminology mapping</td><td>ORU.OBS.CODE.MAP_REQUIRED</td><td>218 open</td><td>0 open</td><td class="good">Recovered</td></tr><tr><td>Contract schema</td><td>Required fields</td><td>0 open</td><td>0 open</td><td class="good">Clean</td></tr><tr><td>MPI reference</td><td>MRN resolves</td><td>0 open</td><td>0 open</td><td class="good">Clean</td></tr></tbody></table>
    </section>
    <section id="warehouse" class="grid">
      <div class="card"><div class="label">Observations</div><div class="metric good">500</div><p>Canonical rows after replay.</p></div>
      <div class="card"><div class="label">Rows check</div><div class="metric good">PASS</div><p>fact_observation_has_rows.</p></div>
      <div class="card"><div class="label">DLQ check</div><div class="metric good">PASS</div><p>open DLQ equals zero.</p></div>
      <div class="card"><div class="label">Incident check</div><div class="metric good">PASS</div><p>incident remediated.</p></div>
    </section>
    <section id="evidence" class="card">
      <div class="label">Evidence package</div>
      <p>This public surface is designed like an operations product. The supporting repo proves the flow with CLI commands, tests, API endpoints, metrics, warehouse checks, and incident report export.</p>
      <span class="pill">No PHI</span><span class="pill">Synthetic data</span><span class="pill">CI gated</span><span class="pill">Replay verified</span><span class="pill">Audit modeled</span>
    </section>
  </main>
</div>
