async function getJson(path: string) {
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  try {
    const res = await fetch(${api}, { cache: "no-store" });
    return await res.json();
  } catch {
    return null;
  }
}

export default async function Page() {
  const summary = await getJson("/summary");
  const incidents = await getJson("/incidents");
  const runs = await getJson("/runs");
  const dlq = await getJson("/dlq");
  const quality = await getJson("/quality");

  return (
    <main style={{ fontFamily: "system-ui", padding: 32, maxWidth: 1200, margin: "0 auto" }}>
      <p style={{ fontWeight: 800, color: "#0f766e", letterSpacing: "0.08em", textTransform: "uppercase" }}>Synthetic demo only · No PHI</p>
      <h1 style={{ fontSize: 56, lineHeight: 1 }}>Pokala HealthOps</h1>
      <h2>Healthcare Interface Operations Platform</h2>
      <p>
        Detect, triage, replay, verify, and audit clinical data pipeline failures using synthetic healthcare data.
      </p>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
        {Object.entries(summary || {}).map(([k, v]) => (
          <div key={k} style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
            <div style={{ color: "#666" }}>{k}</div>
            <div style={{ fontSize: 28, fontWeight: 800 }}>{String(v)}</div>
          </div>
        ))}
      </section>

      <h2>Runs</h2>
      <pre style={{ background: "#f7f7f7", padding: 16, borderRadius: 12, overflow: "auto" }}>{JSON.stringify(runs, null, 2)}</pre>

      <h2>Incidents</h2>
      <pre style={{ background: "#f7f7f7", padding: 16, borderRadius: 12, overflow: "auto" }}>{JSON.stringify(incidents, null, 2)}</pre>

      <h2>Failure Queue</h2>
      <pre style={{ background: "#f7f7f7", padding: 16, borderRadius: 12, overflow: "auto" }}>{JSON.stringify((dlq || []).slice(0, 20), null, 2)}</pre>

      <h2>Quality Checks</h2>
      <pre style={{ background: "#f7f7f7", padding: 16, borderRadius: 12, overflow: "auto" }}>{JSON.stringify(quality, null, 2)}</pre>
    </main>
  );
}
