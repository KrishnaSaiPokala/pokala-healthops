import auditEvents from "../data/evidence/audit-events.json";
import dlqAfter from "../data/evidence/dlq-after.json";
import dlqBefore from "../data/evidence/dlq-before.json";
import incidentReport from "../data/evidence/incident-report.json";
import qualityChecks from "../data/evidence/quality-checks.json";

export function getEvidenceSummary() {
  const counts = incidentReport.counts;
  const passedChecks = qualityChecks.checks.filter((check) => check.status === "pass").length;
  const totalChecks = qualityChecks.checks.length;

  return {
    incident: incidentReport,
    dlqBefore,
    dlqAfter,
    qualityChecks,
    auditEvents,
    metrics: [
      {
        label: "Inbound ORU messages",
        value: counts.inbound_messages.toString(),
        tone: "blue",
        helper: "From incident-report.json"
      },
      {
        label: "Mapping failures",
        value: counts.rejected_before_replay.toString(),
        tone: "red",
        helper: `Rule ${incidentReport.rule_id}`
      },
      {
        label: "Recovered by replay",
        value: counts.replayed_after_fix.toString(),
        tone: "green",
        helper: "Recovered after map remediation"
      },
      {
        label: "Open DLQ",
        value: counts.open_dlq_after_replay.toString(),
        tone: "green",
        helper: "Post-replay DLQ state"
      }
    ],
    checks: qualityChecks.checks,
    passedChecks,
    totalChecks,
    ruleBreakdown: Object.entries(dlqBefore.by_rule).map(([rule, count]) => ({
      rule,
      before: count,
      after: dlqAfter.by_rule[rule as keyof typeof dlqAfter.by_rule] ?? 0
    }))
  };
}
