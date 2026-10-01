# Cloud Lakehouse Blueprint

**Validate a bronze → silver → gold lakehouse before you touch AWS.**

YAML manifests for storage, IAM, lineage, and cost — plus Terraform modules and a Python CLI that plans deploy/rollback in CI. No cloud credentials required to review the design.

[![CI](https://github.com/br413/cloud-lakehouse-blueprint/actions/workflows/ci.yml/badge.svg)](https://github.com/br413/cloud-lakehouse-blueprint/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Terraform AWS](https://img.shields.io/badge/Terraform-AWS-844FBA.svg)](terraform/)

⭐ If this blueprint helps you design a medallion lakehouse, [star the repo](https://github.com/br413/cloud-lakehouse-blueprint) so others can find it.

## Who this is for

- **Data engineers** designing a medallion (bronze → silver → gold) architecture on AWS
- **Platform teams** who want IaC and governance reviewed before any `terraform apply`
- **Hiring managers** evaluating architecture judgment, CI discipline, and portfolio depth

## What you get

| Capability | What it covers |
|------------|----------------|
| Manifest-driven design | YAML for layers, partitioning, access, lineage, and cost |
| Planning CLI | `validate` / `plan` / `cost` / `lineage` / `ddl` — no AWS credentials |
| Terraform modules | S3 storage, IAM roles, Glue catalog — **validate-only** in CI |
| Medallion SQL | Bronze/silver/gold DDL examples under `sql/` |
| CI | pytest + `terraform validate` on every push |

**Intentionally out of scope:** live `terraform apply` against a real AWS account.

## Architecture

```text
manifests (blueprint/*.yml)
        │
        ▼
validate / plan CLI (src/lakehouse)
        │
        ▼
CI (pytest + terraform validate)
        │
        ▼
terraform/  →  storage · iam · catalog
        │
        ▼
medallion SQL (sql/)
```

Data flow example:

```text
orders_api → bronze.raw_orders → silver.stg_orders → gold.fct_daily_orders
```

Details: [`docs/architecture.md`](docs/architecture.md).

## 60-second demo

```bash
git clone https://github.com/br413/cloud-lakehouse-blueprint.git
cd cloud-lakehouse-blueprint
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
python -m src.lakehouse.cli validate
python -m src.lakehouse.cli plan
```

Sample `plan` output:

```text
Deployment plan:
  1. terraform apply storage module -> bronze/silver/gold buckets
  2. terraform apply iam module -> layer-scoped roles
  3. terraform apply catalog module -> glue database and layer tables
  4. create bronze table -> bronze.raw_orders
  ...
  10. validate lineage and access policies -> retail-lakehouse

Rollback plan:
  10. revert blueprint commit and re-run validation (retail-lakehouse)
  ...
  1. terraform destroy -target=module.storage (bronze/silver/gold buckets)
```

Windows one-shot: [`scripts/run_demo.ps1`](scripts/run_demo.ps1).

## Project layout

```text
blueprint/          # YAML manifests (layers, access, lineage, cost, partitioning)
terraform/          # S3 / IAM / Glue modules (validate-only in CI)
sql/                # Medallion DDL examples
src/lakehouse/      # Validation and planning CLI
docs/               # Architecture, ops, ADRs
tests/              # pytest suite
```

## Engineering decisions

Architectural Decision Records live in [`docs/adr/`](docs/adr/). Start with [`0001-manifest-driven-lakehouse.md`](docs/adr/0001-manifest-driven-lakehouse.md).

## Related projects

| Project | Focus |
|---------|-------|
| [production-data-pipeline](https://github.com/br413/production-data-pipeline) | Incremental API ingestion with dbt and Airflow |
| [data-quality-observability](https://github.com/br413/data-quality-observability) | Contract-driven data quality checks with history and alerts |
| [Portfolio](https://br413.github.io) | Senior Data Engineer & Data Architect |

## Writing

| Article | Topic |
|---------|-------|
| [Building a Production Data Pipeline with Incremental Loading and dbt](https://github.com/br413/br413.github.io/blob/main/articles/building-production-data-pipeline.md) | Incremental ingestion, medallion layering, Airflow orchestration |
| [Data Quality Contracts in Production Pipelines](https://github.com/br413/br413.github.io/blob/main/articles/data-quality-contracts-production-pipelines.md) | Quarantine, YAML contracts, alert routing |
| [What I Learned Contributing to Prefect, dbt, and Airflow](https://github.com/br413/br413.github.io/blob/main/articles/oss-upstream-retrospective.md) | Honest OSS retrospective — upstream merges and building in public |
| [Contract Versioning in Production Pipelines](https://github.com/br413/br413.github.io/blob/main/articles/contract-versioning-production-pipelines.md) | Registry, CLI, run history — platform governance context |

## License

MIT — see [LICENSE](LICENSE).

Built by [@br413](https://github.com/br413).
