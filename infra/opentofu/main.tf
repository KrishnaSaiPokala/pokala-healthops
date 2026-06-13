terraform {
  required_version = ">= 1.6.0"
}

locals {
  project_name = "pokala-healthops"
  billing_mode = "local-only"
  services = [
    "fastapi",
    "nextjs",
    "postgres",
    "prometheus",
    "airflow",
    "dbt",
    "kubernetes",
    "helm"
  ]
}

output "project_name" {
  value = local.project_name
}

output "billing_guardrail" {
  value = "No cloud provider resources are declared. Local/reference-only module."
}

output "services" {
  value = local.services
}
