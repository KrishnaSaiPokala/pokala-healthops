from pathlib import Path

# -----------------------------
# Fix timezone warnings safely
# -----------------------------
models = Path("openhip/models.py")
text = models.read_text(encoding="utf-8")
if "from datetime import UTC, datetime" not in text:
    text = text.replace("from datetime import datetime", "from datetime import UTC, datetime")
if "def utc_now() -> datetime:" not in text:
    text = text.replace(
        "from openhip.db import Base\n",
        "from openhip.db import Base\n\n\ndef utc_now() -> datetime:\n    return datetime.now(UTC)\n",
    )
text = text.replace("default=datetime.utcnow", "default=utc_now")
models.write_text(text, encoding="utf-8")

pipeline = Path("openhip/pipeline.py")
text = pipeline.read_text(encoding="utf-8")
if "from datetime import UTC, datetime" not in text:
    text = text.replace("from datetime import datetime", "from datetime import UTC, datetime")
text = text.replace("datetime.utcnow()", "datetime.now(UTC)")
text = text.replace("datetime.utcnow().isoformat()", "datetime.now(UTC).isoformat()")
pipeline.write_text(text, encoding="utf-8")

# -----------------------------
# Add / root endpoint to API
# -----------------------------
api = Path("apps/api/main.py")
text = api.read_text(encoding="utf-8")
if '@app.get("/")' not in text:
    insert = """
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


"""
    text = text.replace('@app.get("/health")', insert + '@app.get("/health")')
api.write_text(text, encoding="utf-8")

# -----------------------------
# Add Windows smoke script
# -----------------------------
Path("scripts").mkdir(exist_ok=True)
Path("scripts/windows_smoke.ps1").write_text(
    r"""$ErrorActionPreference = "Stop"

cd C:\Users\Event\PycharmProjects\HAPI-FHOR-KSP\openhip-command-center

python -m pip install -e ".[dev]"
python -m openhip.cli incident-demo
python -m openhip.cli replay-incident --incident-id INC-20260602-LAB-CODE-FORMAT
python -m openhip.cli verify-warehouse
python -m openhip.cli export-incident-report --incident-id INC-20260602-LAB-CODE-FORMAT
python -m openhip.cli summary
python -m pytest -q
python -m mkdocs build --strict

Write-Host "OpenHIP Windows smoke test completed successfully." -ForegroundColor Green
""",
    encoding="utf-8",
)

# -----------------------------
# Add API test
# -----------------------------
Path("tests/test_api_contract.py").write_text(
    r"""from fastapi.testclient import TestClient

from apps.api.main import app
from openhip.pipeline import incident_demo, replay_incident, verify_warehouse


def test_api_contract_after_replay_recovery():
    incident_demo(total=20, bad_count=5)
    replay_incident()
    verify_warehouse()

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/health").json()["no_phi"] is True
    assert client.get("/summary").json()["dlq_open"] == 0
    assert client.get("/incidents").json()[0]["status"] == "remediated"
    assert all(row["status"] == "passed" for row in client.get("/quality").json())
""",
    encoding="utf-8",
)

# -----------------------------
# Add GitHub Pages workflow
# -----------------------------
Path(".github/workflows").mkdir(parents=True, exist_ok=True)
Path(".github/workflows/pages.yml").write_text(
    r"""name: Deploy Docs to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install --upgrade pip
      - run: pip install -e ".[dev]"
      - run: mkdocs build --strict
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
""",
    encoding="utf-8",
)

# -----------------------------
# Add clean CI workflow
# -----------------------------
Path(".github/workflows/ci.yml").write_text(
    r"""name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install --upgrade pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: python -m openhip.cli incident-demo
      - run: python -m openhip.cli replay-incident --incident-id INC-20260602-LAB-CODE-FORMAT
      - run: python -m openhip.cli verify-warehouse
      - run: pytest -q
      - run: mkdocs build --strict
""",
    encoding="utf-8",
)

# -----------------------------
# Add deployment docs
# -----------------------------
Path("docs/deployment.md").write_text(
    r"""# Deployment

## PyCharm Terminal Smoke Test

Run from PowerShell:

    cd C:\Users\Event\PycharmProjects\HAPI-FHOR-KSP\openhip-command-center
    .\scripts\windows_smoke.ps1

## Local API

    python -m uvicorn apps.api.main:app --reload --host 127.0.0.1 --port 8000

Open:

    http://127.0.0.1:8000/docs

## Local Web UI

    cd apps\web
    npm install
    npm run dev

Open:

    http://localhost:3000

## Public Documentation Target

    https://KrishnaSaiPokala.github.io/openhip-command-center/
""",
    encoding="utf-8",
)

mkdocs = Path("mkdocs.yml")
text = mkdocs.read_text(encoding="utf-8")
if "Deployment: deployment.md" not in text:
    text = text.replace(
        "      - Security: security.md\n      - Interview Story: interview-story.md",
        "      - Security: security.md\n      - Deployment: deployment.md\n      - Interview Story: interview-story.md",
    )
mkdocs.write_text(text, encoding="utf-8")

# -----------------------------
# Improve README
# -----------------------------
readme = Path("README.md")
text = readme.read_text(encoding="utf-8")
extra = """
## Windows / PyCharm Terminal Workflow

    cd C:\\Users\\Event\\PycharmProjects\\HAPI-FHOR-KSP\\openhip-command-center
    .\\scripts\\windows_smoke.ps1

## Public Documentation Target

    https://KrishnaSaiPokala.github.io/openhip-command-center/

## Current Verified Core Flow

- Synthetic ORU ingestion
- Terminology mapping failure
- DLQ creation
- Incident creation
- Mapping remediation
- DLQ replay
- Warehouse-quality verification
- Incident evidence export
- MkDocs documentation build
"""
if "## Windows / PyCharm Terminal Workflow" not in text:
    text = text.rstrip() + "\n\n" + extra
readme.write_text(text, encoding="utf-8")

print("OpenHIP hardening patch completed.")
