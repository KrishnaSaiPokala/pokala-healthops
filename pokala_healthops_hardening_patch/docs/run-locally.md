# Run locally

## Python demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

python -m openhip.cli incident-demo
python -m openhip.cli replay-incident
python -m openhip.cli verify-warehouse
python -m openhip.cli export-incident-report
```

## API

```bash
uvicorn apps.api.main:app --reload --port 8000
```

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/health` | Service health |
| `/summary` | Current summary counts |
| `/runs` | Integration runs |
| `/incidents` | Incident records |
| `/dlq` | Dead-letter records |
| `/terminology` | Terminology map records |
| `/observations` | Accepted observations |
| `/metrics` | Prometheus metrics |

## Web app

```bash
cd apps/web
npm install
npm run typecheck
npm run build
npm run dev
```

## Docs

```bash
mkdocs build --strict
```

## Clean state

```bash
make clean
```
