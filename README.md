# Cloud Lakehouse Blueprint

> **Medallion lakehouse architecture blueprint** with YAML manifests, Terraform infrastructure-as-code, IAM governance, lineage tracking, and CI validation — a reference for data architects designing cloud data platforms on AWS.

[![CI](https://github.com/br413/cloud-lakehouse-blueprint/actions/workflows/ci.yml/badge.svg)](https://github.com/br413/cloud-lakehouse-blueprint/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=flat-square&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20IAM%20%7C%20Glue-232F3E?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

A **data architecture** portfolio project demonstrating how to define bronze/silver/gold lakehouse layers, access controls, partitioning, lineage, and cost models as reviewable code — before deploying to production cloud infrastructure.

## Why this project exists

Teams adopt lakehouses faster when storage, access, partitioning, lineage, and deployment plans are defined together—not as scattered wiki pages. This repository demonstrates a reviewable blueprint you can validate in CI before touching production cloud resources.

**Ideal for:** data architects planning medallion architectures, platform engineers evaluating Terraform lakehouse modules, and teams migrating from data warehouses to lakehouse patterns.

## Architecture

```text
Blueprint manifests (YAML)
    ↓
Validation + planning CLI
    ↓
Terraform modules
    ├── storage (bronze/silver/gold)
    ├── iam (layer-scoped roles)
    └── catalog (governed metadata)
    ↓
Medallion SQL assets
    ↓
Analytics consumers
```

See [`docs/architecture.md`](docs/architecture.md) for layer boundaries and governance model.

## Current capabilities

- [x] Bronze/silver/gold manifest with table lineage
- [x] Partitioning strategy per table with DDL rendering
- [x] Role-based access controls with policy validation
- [x] Lineage graph and governance metadata
- [x] Cost and performance estimation model
- [x] Deployment and rollback plan generation
- [x] Terraform modules for storage, IAM, and catalog
- [x] pytest validation suite and GitHub Actions CI
- [x] `validate --json` output for CI and automation pipelines
- [ ] Live cloud deployment (Terraform validate only in CI)

## Technology stack

| Area | Selection |
|------|-----------|
| Blueprint | YAML manifests |
| IaC | Terraform (AWS S3, IAM, Glue) |
| Tooling | Python 3.12 CLI |
| SQL | Medallion layer DDL examples |
| Testing | pytest + `terraform validate` |
| Governance | Lineage + PII classification metadata |

## Quick start

```bash
git clone https://github.com/br413/cloud-lakehouse-blueprint.git
cd cloud-lakehouse-blueprint
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
python -m src.lakehouse.cli validate
python -m src.lakehouse.cli plan
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m src.lakehouse.cli validate
python -m src.lakehouse.cli plan
```

Run the demo script (Windows):

```powershell
.\scripts\run_demo.ps1
```

Validate with JSON output for CI pipelines:

```bash
python -m src.lakehouse.cli validate --json
```

## Project structure

```text
.
├── blueprint/           # lakehouse, partitioning, access, lineage, cost
├── terraform/           # storage, iam, catalog modules
├── sql/                 # medallion DDL examples
├── src/lakehouse/       # validation and planning CLI
├── docs/
├── tests/
└── scripts/
```

## Engineering decisions

Architectural Decision Records are stored in [`docs/adr/`](docs/adr/).

## Testing

```bash
pytest -v
cd terraform && terraform init -backend=false && terraform validate
```

## Operations

| Concern | Approach |
|---------|----------|
| Deployment | [`docs/deployment.md`](docs/deployment.md) |
| Day-2 ops | [`docs/operations.md`](docs/operations.md) |
| Rollback | Reverse-order plan from CLI `plan` |
| Access | Layer-scoped IAM roles |
| Cost | [`docs/cost-performance.md`](docs/cost-performance.md) |
| Governance | [`docs/governance.md`](docs/governance.md) |

## Platform stack demo

This repo defines **governance and IaC** for the medallion layers that companion projects implement:

| Layer | Runnable project |
|-------|------------------|
| Ingest + transform | [production-data-pipeline](https://github.com/br413/production-data-pipeline) |
| Quality contracts | [data-quality-observability](https://github.com/br413/data-quality-observability) |
| Runnable lakehouse | [lakehouse-platform-starter](https://github.com/br413/lakehouse-platform-starter) |

Suggested flow: validate manifests here (`python -m src.lakehouse.cli validate`), then explore ingestion + contract checks in the pipeline and quality repos.

## Related projects

| Project | Focus |
|---------|-------|
| [**production-data-pipeline**](https://github.com/br413/production-data-pipeline) | Incremental API ingestion with dbt and Airflow |
| [**data-quality-observability**](https://github.com/br413/data-quality-observability) | Contract-driven data quality checks with history and alerts |
| [**@br413**](https://github.com/br413) | Senior Data Engineer & Data Architect portfolio |

## Writing

| Article | Topic |
|---------|-------|
| [Building a Production Data Pipeline with Incremental Loading and dbt](https://dev.to/bobby_ray_581732c715283b2/building-a-production-data-pipeline-with-incremental-loading-and-dbt-2e2c) | Incremental ingestion, medallion layering, Airflow orchestration |
| [Data Quality Contracts in Production Pipelines](https://dev.to/bobby_ray_581732c715283b2/data-quality-contracts-in-production-pipelines-without-a-separate-platform-team-f3) | Quarantine, YAML contracts, alert routing |
| [What I Learned Contributing to Prefect, dbt, and Airflow](https://dev.to/bobby_ray_581732c715283b2/what-i-learned-contributing-to-prefect-dbt-and-airflow-an-honest-oss-retrospective-1ki8) | Honest OSS retrospective — upstream merges and building in public |
| [Contract Versioning in Production Pipelines](https://dev.to/bobby_ray_581732c715283b2/contract-versioning-in-production-pipelines-registry-cli-and-run-history-13el) | Registry, CLI, run history — platform governance context |

## Topics

`lakehouse` · `data-architecture` · `medallion-architecture` · `terraform` · `data-engineering` · `data-platform` · `aws` · `bronze-silver-gold` · `lineage` · `governance` · `infrastructure-as-code`

## Attribution

Built as a public portfolio project by [@br413](https://github.com/br413) — Senior Data Engineer & Data Architect. Terraform targets AWS primitives as a reference implementation; adapt modules for your cloud provider.

## License

MIT — see [LICENSE](LICENSE).
