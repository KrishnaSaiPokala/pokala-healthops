SHELL := /bin/bash
PYTHON ?= python3

.PHONY: bootstrap check test lint api web web-build demo incident-demo replay-incident \
        verify-warehouse export-incident-report evidence mpi-demo docs clean

bootstrap:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -e ".[dev]"
	@echo "Done. Run: source .venv/bin/activate"

check: lint test

lint:
	. .venv/bin/activate && ruff check . && mypy openhip apps/api

test:
	. .venv/bin/activate && pytest -q

api:
	. .venv/bin/activate && uvicorn apps.api.main:app --reload --port 8000

web:
	cd apps/web && npm install && npm run dev

web-build:
	cd apps/web && npm install && npm run typecheck && npm run build

demo:
	. .venv/bin/activate && python -m openhip.cli demo

incident-demo:
	. .venv/bin/activate && python -m openhip.cli incident-demo

replay-incident:
	. .venv/bin/activate && python -m openhip.cli replay-incident

verify-warehouse:
	. .venv/bin/activate && python -m openhip.cli verify-warehouse

export-incident-report:
	. .venv/bin/activate && python -m openhip.cli export-incident-report

evidence: incident-demo replay-incident verify-warehouse export-incident-report
	@mkdir -p evidence
	@cp -f reports/INC-20260602-LAB-CODE-FORMAT.json evidence/incident-report.generated.json || true
	@echo "Evidence command completed. Generated runtime report is under evidence/ if available."

mpi-demo:
	. .venv/bin/activate && python -m openhip.cli mpi-demo

docs:
	. .venv/bin/activate && mkdocs build --strict

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache reports site openhip.db
