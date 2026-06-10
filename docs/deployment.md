# Deployment

## PyCharm Terminal Smoke Test

Run from PowerShell:

    cd C:\Users\Event\PycharmProjects\HAPI-FHOR-KSP\openhip-command-center
    .\scripts\windows_smoke.ps1

## Local API

    python -m uvicorn apps.api.main:app --reload --host 127.0.0.1 --port 8000

Open:

    http://127.0.0.1:8000/
    http://127.0.0.1:8000/docs

## Local Web UI

    cd apps\web
    npm install
    npm run dev

Open:

    http://localhost:3000

## Public Documentation Target

    https://KrishnaSaiPokala.github.io/openhip-command-center/
