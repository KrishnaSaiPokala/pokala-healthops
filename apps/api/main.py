from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from sqlalchemy import select

from openhip.db import SessionLocal, init_db
from openhip.metrics import render_metrics
from openhip.models import DeadLetterMessage, Incident, IntegrationRun, Observation, TerminologyMap
from openhip.pipeline import (
    export_incident_report,
    incident_demo,
    replay_incident,
    summarize,
    verify_warehouse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Pokala HealthOps API", version="0.9.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "no_phi": True}


@app.get("/summary")
def summary() -> dict:
    return summarize()


@app.post("/incident-demo")
def run_incident() -> dict:
    return incident_demo()


@app.post("/replay/{incident_id}")
def replay(incident_id: str) -> dict:
    return replay_incident(incident_id)


@app.post("/verify-warehouse")
def verify() -> dict:
    return verify_warehouse()


@app.post("/export-incident-report/{incident_id}")
def export(incident_id: str) -> dict:
    return {"path": str(export_incident_report(incident_id))}


@app.get("/runs")
def runs() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(IntegrationRun).order_by(IntegrationRun.id.desc())).all()
        return [{
            "run_id": r.run_id, "status": r.status, "inbound": r.inbound_count,
            "accepted": r.accepted_count, "rejected": r.rejected_count,
            "reject_rate": r.reject_rate, "sla_status": r.sla_status,
            "incident_id": r.incident_id,
        } for r in rows]


@app.get("/incidents")
def incidents() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(Incident).order_by(Incident.id.desc())).all()
        return [{
            "incident_id": i.incident_id, "severity": i.severity, "status": i.status,
            "primary_failure": i.primary_failure, "failed_rule": i.failed_rule,
            "failed_messages": i.failed_messages, "remediation_summary": i.remediation_summary,
        } for i in rows]


@app.get("/dlq")
def dlq() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(
            select(DeadLetterMessage).order_by(DeadLetterMessage.id.desc()).limit(200)
        ).all()
        return [{
            "dlq_id": d.dlq_id, "message_id": d.original_message_id,
            "failure_category": d.failure_category, "failed_rule_id": d.failed_rule_id,
            "error_message": d.error_message, "status": d.status,
            "last_replay_status": d.last_replay_status,
        } for d in rows]


@app.get("/terminology")
def terminology() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(TerminologyMap).order_by(TerminologyMap.id)).all()
        return [{
            "source_code": m.source_code, "target_code": m.target_code,
            "target_display": m.target_display, "version": m.version,
        } for m in rows]


@app.get("/observations")
def observations() -> list[dict]:
    with SessionLocal() as db:
        rows = db.scalars(select(Observation).order_by(Observation.id.desc()).limit(100)).all()
        return [{
            "observation_id": o.observation_id, "patient_id": o.patient_id,
            "source_code": o.source_code, "target_code": o.target_code,
            "value_numeric": o.value_numeric, "unit": o.unit,
            "match_type": o.match_type, "abnormal_flag": o.abnormal_flag,
        } for o in rows]


@app.get("/metrics")
def metrics() -> Response:
    body, content_type = render_metrics()
    return Response(content=body, media_type=content_type)
