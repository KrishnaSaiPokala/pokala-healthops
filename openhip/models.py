from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from openhip.db import Base


class IntegrationRun(Base):
    __tablename__ = "integration_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    source_interface: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default="running")
    inbound_count: Mapped[int] = mapped_column(Integer, default=0)
    accepted_count: Mapped[int] = mapped_column(Integer, default=0)
    rejected_count: Mapped[int] = mapped_column(Integer, default=0)
    reject_rate: Mapped[float] = mapped_column(Float, default=0.0)
    sla_status: Mapped[str] = mapped_column(String, default="unknown")
    incident_id: Mapped[str | None] = mapped_column(String, nullable=True)


class RawMessage(Base):
    __tablename__ = "raw_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String, index=True)
    message_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    interface_name: Mapped[str] = mapped_column(String)
    payload: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="inbound")
    trace_id: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[str] = mapped_column(String, unique=True)
    mrn: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    dob: Mapped[str] = mapped_column(String)
    zip3: Mapped[str] = mapped_column(String, default="000")


class Encounter(Base):
    __tablename__ = "encounters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    encounter_id: Mapped[str] = mapped_column(String, unique=True)
    patient_id: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, default="active")


class TerminologyMap(Base):
    __tablename__ = "terminology_map"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_system: Mapped[str] = mapped_column(String, default="demo_lab_lis")
    source_code: Mapped[str] = mapped_column(String, unique=True, index=True)
    source_display: Mapped[str] = mapped_column(String)
    target_system: Mapped[str] = mapped_column(String, default="http://loinc.org/demo")
    target_code: Mapped[str] = mapped_column(String)
    target_display: Mapped[str] = mapped_column(String)
    map_status: Mapped[str] = mapped_column(String, default="active")
    version: Mapped[str] = mapped_column(String, default="lab_map_v1")
    updated_by: Mapped[str] = mapped_column(String, default="demo_analyst")


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    observation_id: Mapped[str] = mapped_column(String, unique=True)
    run_id: Mapped[str] = mapped_column(String, index=True)
    source_message_id: Mapped[str] = mapped_column(String, index=True)
    patient_id: Mapped[str] = mapped_column(String, index=True)
    encounter_id: Mapped[str] = mapped_column(String, index=True)
    source_code: Mapped[str] = mapped_column(String)
    target_code: Mapped[str] = mapped_column(String)
    target_display: Mapped[str] = mapped_column(String)
    value_numeric: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    abnormal_flag: Mapped[str] = mapped_column(String, default="N")
    observation_datetime: Mapped[str] = mapped_column(String)
    match_type: Mapped[str] = mapped_column(String, default="exact_match")
    match_confidence: Mapped[float] = mapped_column(Float, default=1.0)


class DeadLetterMessage(Base):
    __tablename__ = "dead_letter_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dlq_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    original_message_id: Mapped[str] = mapped_column(String, index=True)
    run_id: Mapped[str] = mapped_column(String, index=True)
    incident_id: Mapped[str | None] = mapped_column(String, nullable=True)
    interface_name: Mapped[str] = mapped_column(String)
    topic: Mapped[str] = mapped_column(String)
    failure_category: Mapped[str] = mapped_column(String)
    failed_rule_id: Mapped[str] = mapped_column(String)
    error_message: Mapped[str] = mapped_column(Text)
    raw_payload: Mapped[str] = mapped_column(Text)
    patient_key: Mapped[str] = mapped_column(String)
    trace_id: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="open")
    replay_count: Mapped[int] = mapped_column(Integer, default=0)
    last_replay_status: Mapped[str | None] = mapped_column(String, nullable=True)
    remediation_id: Mapped[str | None] = mapped_column(String, nullable=True)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    severity: Mapped[str] = mapped_column(String, default="medium")
    source_interface: Mapped[str] = mapped_column(String)
    primary_failure: Mapped[str] = mapped_column(String)
    failed_rule: Mapped[str] = mapped_column(String)
    failed_messages: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String, default="open")
    opened_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    remediation_summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_event_id: Mapped[str] = mapped_column(String, unique=True)
    event_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actor_id: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    resource_type: Mapped[str] = mapped_column(String)
    resource_id: Mapped[str] = mapped_column(String)
    outcome: Mapped[str] = mapped_column(String)
    run_id: Mapped[str] = mapped_column(String)
    trace_id: Mapped[str] = mapped_column(String)


class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String, index=True)
    check_name: Mapped[str] = mapped_column(String)
    domain: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    impacted_rows: Mapped[int] = mapped_column(Integer, default=0)
    detail: Mapped[str] = mapped_column(Text, default="")
