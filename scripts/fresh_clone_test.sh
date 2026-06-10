#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
python -m openhip.cli incident-demo
python -m openhip.cli replay-incident --incident-id INC-20260602-LAB-CODE-FORMAT
python -m openhip.cli verify-warehouse
pytest -q
mkdocs build
