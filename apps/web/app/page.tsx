async function getJson(path: string) {
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  try {
    const res = await fetch(`${api}${path}`, { cache: "no-store" });
    return await res.json();
  } catch {
    return null;
  }
}

function Card({ label, value }: { label: string; value: any }) {
  return (
    <div style={{ border: "1px solid #232733", borderRadius: 10, padding: "16px 18px",
      background: "#151823" }}>
      <div style={{ color: "#8b93a7", fontSize: 13, textTransform: "uppercase",
        letterSpacing: 0.5 }}>{label}</div>
      <div style={{ fontSize: 30, fontWeight: 700, marginTop: 6 }}>{String(value)}</div>
    </div>
  );
}

export default async function Page() {
  const summary = await getJson("/summary");
  const incidents = (await getJson("/incidents")) || [];
  const dlq = (await getJson("/dlq")) || [];
  const top = incidents[0];

  return (
    <main style={{ maxWidth: 1080, margin: "0 auto", padding: "40px 24px" }}>
      <div style={{ color: "#8b93a7", fontSize: 13, letterSpacing: 1 }}>
        SYNTHETIC DATA · NO PHI
      </div>
      <h1 style={{ fontSize: 30, margin: "8px 0 4px" }}>Pokala HealthOps</h1>
      <p style={{ color: "#aab2c5", maxWidth: 720 }}>
        Healthcare interface operations: ingest, validate against a data contract,
        resolve identity, map terminology, and replay anything that fails.
      </p>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
        gap: 14, margin: "26px 0" }}>
        <Card label="Messages" value={summary?.raw_messages ?? "-"} />
        <Card label="Observations" value={summary?.observations ?? "-"} />
        <Card label="Open DLQ" value={summary?.dlq_open ?? "-"} />
        <Card label="Incidents" value={summary?.incidents ?? "-"} />
      </section>

      {top && (
        <section style={{ border: "1px solid #232733", borderRadius: 10, padding: 18,
          background: "#151823", marginBottom: 26 }}>
          <h2 style={{ marginTop: 0, fontSize: 18 }}>{top.incident_id}</h2>
          <p style={{ color: "#aab2c5", margin: "4px 0" }}>
            {top.primary_failure} · rule {top.failed_rule} · status{" "}
            <b style={{ color: top.status === "remediated" ? "#5ad19a" : "#e0b341" }}>
              {top.status}</b>
          </p>
          <p style={{ color: "#8b93a7", margin: 0 }}>{top.remediation_summary}</p>
        </section>
      )}

      <h2 style={{ fontSize: 18 }}>Failure queue</h2>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
        <thead>
          <tr style={{ textAlign: "left", color: "#8b93a7" }}>
            <th style={{ padding: 8 }}>Message</th>
            <th style={{ padding: 8 }}>Category</th>
            <th style={{ padding: 8 }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {dlq.slice(0, 12).map((d: any) => (
            <tr key={d.dlq_id} style={{ borderTop: "1px solid #232733" }}>
              <td style={{ padding: 8, fontFamily: "ui-monospace" }}>{d.message_id}</td>
              <td style={{ padding: 8 }}>{d.failure_category}</td>
              <td style={{ padding: 8 }}>{d.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
