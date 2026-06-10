from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from sqlalchemy import select

from openhip.db import SessionLocal, init_db
from openhip.models import (
    DeadLetterMessage,
    Incident,
    IntegrationRun,
    Observation,
    QualityCheck,
    TerminologyMap,
)
from openhip.pipeline import (
    demo_run,
    export_incident_report,
    incident_demo,
    prometheus_metrics,
    replay_incident,
    summarize,
    verify_warehouse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="OpenHIP Command Center API",
    description="Local-first no-PHI InterfaceOps API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict:
    return {
        "name": "OpenHIP Command Center",
        "status": "ok",
        "no_phi": True,
        "docs": "/docs",
        "health": "/health",
        "summary": "/summary",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "no_phi": True}


@app.get("/summary")
def summary() -> dict:
    return summarize()


@app.post("/demo")
def run_demo() -> dict:
    return demo_run()


@app.post("/incident-demo")
def run_incident_demo() -> dict:
    return incident_demo()


@app.post("/replay/{incident_id}")
def replay(incident_id: str) -> dict:
    return replay_incident(incident_id)


@app.post("/verify-warehouse")
def verify() -> dict:
    return verify_warehouse()


@app.post("/export-incident-report/{incident_id}")
def export_report(incident_id: str) -> dict:
    path = export_incident_report(incident_id)
    return {"path": str(path)}


@app.get("/runs")
def runs() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(IntegrationRun).order_by(IntegrationRun.id.desc())).all()
        return [
            {
                "run_id": r.run_id,
                "source_interface": r.source_interface,
                "status": r.status,
                "inbound_count": r.inbound_count,
                "accepted_count": r.accepted_count,
                "rejected_count": r.rejected_count,
                "reject_rate": r.reject_rate,
                "sla_status": r.sla_status,
                "incident_id": r.incident_id,
            }
            for r in rows
        ]


@app.get("/incidents")
def incidents() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(Incident).order_by(Incident.id.desc())).all()
        return [
            {
                "incident_id": i.incident_id,
                "severity": i.severity,
                "status": i.status,
                "source_interface": i.source_interface,
                "primary_failure": i.primary_failure,
                "failed_rule": i.failed_rule,
                "failed_messages": i.failed_messages,
                "remediation_summary": i.remediation_summary,
            }
            for i in rows
        ]


@app.get("/dlq")
def dlq() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(
            select(DeadLetterMessage).order_by(DeadLetterMessage.id.desc()).limit(500)
        ).all()
        return [
            {
                "dlq_id": d.dlq_id,
                "incident_id": d.incident_id,
                "message_id": d.original_message_id,
                "failure_category": d.failure_category,
                "failed_rule_id": d.failed_rule_id,
                "error_message": d.error_message,
                "patient_key": d.patient_key,
                "status": d.status,
                "replay_count": d.replay_count,
                "last_replay_status": d.last_replay_status,
            }
            for d in rows
        ]


@app.get("/terminology")
def terminology() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(TerminologyMap).order_by(TerminologyMap.id)).all()
        return [
            {
                "source_code": m.source_code,
                "source_display": m.source_display,
                "target_code": m.target_code,
                "target_display": m.target_display,
                "version": m.version,
                "updated_by": m.updated_by,
            }
            for m in rows
        ]


@app.get("/observations")
def observations() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(Observation).order_by(Observation.id.desc()).limit(100)).all()
        return [
            {
                "observation_id": o.observation_id,
                "patient_id": o.patient_id,
                "source_code": o.source_code,
                "target_code": o.target_code,
                "value_numeric": o.value_numeric,
                "unit": o.unit,
                "abnormal_flag": o.abnormal_flag,
            }
            for o in rows
        ]


@app.get("/quality")
def quality() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(QualityCheck).order_by(QualityCheck.id.desc())).all()
        return [
            {
                "run_id": q.run_id,
                "check_name": q.check_name,
                "domain": q.domain,
                "status": q.status,
                "impacted_rows": q.impacted_rows,
                "detail": q.detail,
            }
            for q in rows
        ]


@app.get("/metrics")
def metrics() -> Response:
    return Response(content=prometheus_metrics(), media_type="text/plain")
