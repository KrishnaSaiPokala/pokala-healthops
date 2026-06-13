from __future__ import annotations

from datetime import datetime

from airflow.operators.bash import BashOperator

from airflow import DAG

DEFAULT_ARGS = {"owner": "healthops", "depends_on_past": False, "retries": 0}

with DAG(
    dag_id="healthops_incident_recovery_evidence",
    default_args=DEFAULT_ARGS,
    description="Local-only DAG for no-PHI replay, verification, and evidence export.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["healthops", "reliability", "no-phi", "evidence"],
) as dag:
    incident_demo = BashOperator(
        task_id="incident_demo",
        bash_command="cd /opt/airflow/project && python -m openhip.cli incident-demo",
    )

    replay_incident = BashOperator(
        task_id="replay_incident",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m openhip.cli replay-incident "
            "--incident-id INC-20260602-LAB-CODE-FORMAT"
        ),
    )

    verify_replay_invariants = BashOperator(
        task_id="verify_replay_invariants",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m openhip.cli verify-replay-invariants"
        ),
    )

    verify_warehouse = BashOperator(
        task_id="verify_warehouse",
        bash_command="cd /opt/airflow/project && python -m openhip.cli verify-warehouse",
    )

    export_incident_report = BashOperator(
        task_id="export_incident_report",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m openhip.cli export-incident-report "
            "--incident-id INC-20260602-LAB-CODE-FORMAT"
        ),
    )

    (
        incident_demo
        >> replay_incident
        >> verify_replay_invariants
        >> verify_warehouse
        >> export_incident_report
    )
