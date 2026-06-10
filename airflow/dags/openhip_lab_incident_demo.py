from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="openhip_lab_incident_demo",
    start_date=datetime(2026, 6, 2),
    schedule=None,
    catchup=False,
    tags=["openhip", "interfaceops", "no-phi"],
) as dag:
    incident_demo = BashOperator(
        task_id="incident_demo",
        bash_command="cd /opt/openhip && python -m openhip.cli incident-demo",
    )

    replay = BashOperator(
        task_id="replay_incident",
        bash_command="cd /opt/openhip && python -m openhip.cli replay-incident --incident-id INC-20260602-LAB-CODE-FORMAT",
    )

    verify = BashOperator(
        task_id="verify_warehouse",
        bash_command="cd /opt/openhip && python -m openhip.cli verify-warehouse",
    )

    export = BashOperator(
        task_id="export_incident_report",
        bash_command="cd /opt/openhip && python -m openhip.cli export-incident-report --incident-id INC-20260602-LAB-CODE-FORMAT",
    )

    incident_demo >> replay >> verify >> export
