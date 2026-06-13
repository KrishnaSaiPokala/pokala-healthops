# Local Platform Stack

This project intentionally uses a zero-cloud-bill platform stack.

## Local/free tools

- Docker / Docker Compose
- kind local Kubernetes
- kubectl
- Helm
- OpenTofu local validation
- dbt Core with DuckDB
- Prometheus
- Airflow DAG definition
- Next.js
- FastAPI

## Billing guardrail

No AWS, GCP, Azure, Terraform Cloud, dbt Cloud, Astronomer Cloud, or Grafana Cloud
resources are required by this stack.

The platform assets are production-shaped, but local-first:

- `docker-compose.yml` runs local services.
- `deploy/kubernetes/` contains local kind-compatible manifests.
- `deploy/helm/healthops/` packages the local Kubernetes deployment.
- `warehouse/` contains dbt Core models using DuckDB.
- `orchestration/airflow/` contains a DAG for incident recovery evidence.
- `observability/prometheus/` contains local scrape configuration.
- `infra/opentofu/` contains local/reference-only IaC outputs with no cloud resources.

## Portfolio signal

This stack shows cloud-native platform skills without creating paid infrastructure:

- containerization
- Kubernetes deployment modeling
- Helm packaging
- workflow orchestration
- warehouse modeling and tests
- observability configuration
- infrastructure-as-code guardrails
