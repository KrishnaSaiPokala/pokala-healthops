SHELL := /bin/bash
PYTHON ?= python3

.PHONY: bootstrap up down api web demo incident-demo replay-incident verify-warehouse export-incident-report test lint docs clean

bootstrap:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -e ".[dev]"
	@echo "Bootstrap complete. Run: source .venv/bin/activate"

up:
	docker compose up --build

down:
	docker compose down -v

api:
	. .venv/bin/activate && uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd apps/web && npm install && npm run dev

demo:
	. .venv/bin/activate && python -m openhip.cli demo

incident-demo:
	. .venv/bin/activate && python -m openhip.cli incident-demo

replay-incident:
	. .venv/bin/activate && python -m openhip.cli replay-incident --incident-id INC-20260602-LAB-CODE-FORMAT

verify-warehouse:
	. .venv/bin/activate && python -m openhip.cli verify-warehouse

export-incident-report:
	. .venv/bin/activate && python -m openhip.cli export-incident-report --incident-id INC-20260602-LAB-CODE-FORMAT

test:
	. .venv/bin/activate && pytest -q

lint:
	. .venv/bin/activate && ruff check . && mypy openhip apps/api

docs:
	. .venv/bin/activate && mkdocs build

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache reports site openhip.db
