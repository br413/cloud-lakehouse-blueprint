# cloud-lakehouse-blueprint

> Infrastructure-as-code and manifest-driven blueprint for a bronze/silver/gold cloud lakehouse.

## Why this project exists

Teams adopt lakehouses faster when storage, access, partitioning, lineage, and deployment plans are defined together—not as scattered wiki pages. This repository demonstrates a reviewable blueprint you can validate in CI before touching production cloud resources.

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
- [ ] Live cloud deployment (Terraform validate only in CI)

## Technology

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
| Rollback | Reverse-order plan from CLI `plan` |
| Access | Layer-scoped IAM roles |
| Cost | [`docs/cost-performance.md`](docs/cost-performance.md) |
| Governance | [`docs/governance.md`](docs/governance.md) |

## Related work

- [`production-data-pipeline`](https://github.com/br413/production-data-pipeline) — incremental ingestion
- [`data-quality-observability`](https://github.com/br413/data-quality-observability) — contract-driven quality checks

## Attribution

Built as a public portfolio project by [@br413](https://github.com/br413). Terraform targets AWS primitives as a reference implementation; adapt modules for your cloud provider.

## License

MIT — see [LICENSE](LICENSE).
