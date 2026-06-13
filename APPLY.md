# Apply this patch bundle

The GitHub connector did not have push permission for `KrishnaSaiPokala/pokala-healthops`, so this bundle is structured as direct file replacements.

From the repository root:

```bash
cp -R path/to/pokala_healthops_hardening_patch/. .

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make check
make incident-demo
make replay-incident
make verify-warehouse
make export-incident-report
make docs
make web-build
```

Then commit:

```bash
git checkout -b hardening/truth-evidence-ci
git add .
git commit -m "Harden project claims, evidence, docs, and frontend gate"
git push origin hardening/truth-evidence-ci
```
