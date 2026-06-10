$ErrorActionPreference = "Stop"

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
