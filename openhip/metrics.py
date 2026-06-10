from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest
from sqlalchemy import func, select

from openhip.db import SessionLocal, init_db
from openhip.models import DeadLetterMessage, Observation, RawMessage


def render_metrics() -> tuple[bytes, str]:
    init_db()
    registry = CollectorRegistry()
    inbound = Gauge("openhip_messages_inbound", "Inbound messages", registry=registry)
    accepted = Gauge("openhip_messages_accepted", "Accepted observations", registry=registry)
    rejected = Gauge("openhip_messages_rejected", "Dead-letter messages", registry=registry)
    open_dlq = Gauge("openhip_deadletter_open", "Open dead-letter messages", registry=registry)
    reject_rate = Gauge("openhip_contract_reject_rate", "Reject rate", registry=registry)

    with SessionLocal() as db:
        total = db.scalar(select(func.count(RawMessage.id))) or 0
        obs = db.scalar(select(func.count(Observation.id))) or 0
        dlq = db.scalar(select(func.count(DeadLetterMessage.id))) or 0
        still_open = db.scalar(
            select(func.count(DeadLetterMessage.id)).where(DeadLetterMessage.status == "open")
        ) or 0

    inbound.set(total)
    accepted.set(obs)
    rejected.set(dlq)
    open_dlq.set(still_open)
    reject_rate.set(dlq / total if total else 0.0)
    return generate_latest(registry), CONTENT_TYPE_LATEST
