# Architecture

## Medallion layers

| Layer | Purpose | Format | Retention |
|-------|---------|--------|-----------|
| Bronze | Raw landing | Parquet | 90 days |
| Silver | Cleaned entities | Delta | 365 days |
| Gold | Business aggregates | Delta | 730 days |

## Component map

| Component | Responsibility |
|-----------|----------------|
| `blueprint/lakehouse.yml` | Layer and table definitions |
| `blueprint/partitioning.yml` | Partition keys and granularity |
| `blueprint/access.yml` | Role-based layer permissions |
| `blueprint/lineage.yml` | Source-to-consumer graph |
| `blueprint/cost.yml` | Cost and performance assumptions |
| `terraform/modules/storage` | Layer-scoped object storage |
| `terraform/modules/iam` | Least-privilege roles |
| `terraform/modules/catalog` | Governed metadata catalog |
| `src/lakehouse/cli.py` | Validation and planning entry point |

## Data flow

```text
orders_api ──► bronze.raw_orders ──► silver.stg_orders ──► gold.fct_daily_orders ──► bi_dashboard
crm_export ──► bronze.raw_customers ──► silver.dim_customers ──► gold.rpt_customer_summary ──► bi_dashboard
```

## Partitioning strategy

- **Date partitions** on high-volume fact tables (`updated_at`, `order_date`)
- **Region partitions** on dimension tables with geographic query patterns
- Target: 35% compute savings from partition pruning (see `blueprint/cost.yml`)

## Access model

| Role | Bronze | Silver | Gold | Deploy |
|------|--------|--------|------|--------|
| data_engineer | RW | RW | RW | Yes |
| analytics_engineer | — | RW | RW | No |
| analyst | — | — | R | No |
| auditor | R | R | R | No |

## Design choices

- Manifest-first blueprint keeps review surface small
- Terraform modules map 1:1 to operational boundaries
- Validation runs without cloud credentials

See [`docs/adr/0001-manifest-driven-lakehouse.md`](adr/0001-manifest-driven-lakehouse.md).
