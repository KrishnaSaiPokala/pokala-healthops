import json

import typer
from rich import print

from openhip.pipeline import (
    demo_run,
    export_incident_report,
    incident_demo,
    mpi_demo,
    replay_incident,
    summarize,
    verify_warehouse,
)

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("demo")
def demo() -> None:
    print(json.dumps(demo_run(), indent=2))


@app.command("incident-demo")
def incident() -> None:
    print(json.dumps(incident_demo(), indent=2))


@app.command("replay-incident")
def replay(incident_id: str = typer.Option("INC-20260602-LAB-CODE-FORMAT")) -> None:
    print(json.dumps(replay_incident(incident_id), indent=2))


@app.command("verify-warehouse")
def verify() -> None:
    print(json.dumps(verify_warehouse(), indent=2))


@app.command("export-incident-report")
def export(incident_id: str = typer.Option("INC-20260602-LAB-CODE-FORMAT")) -> None:
    print(f"[green]Exported[/green] {export_incident_report(incident_id)}")


@app.command("mpi-demo")
def mpi() -> None:
    print(json.dumps(mpi_demo(), indent=2))


@app.command("summary")
def summary() -> None:
    print(json.dumps(summarize(), indent=2))


if __name__ == "__main__":
    app()
