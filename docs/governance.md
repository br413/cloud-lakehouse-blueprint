# Governance

## Ownership

- **Platform owner:** data-platform (from `blueprint/lineage.yml`)
- **Classification:** internal
- **PII columns:** `silver.dim_customers.full_name`

## Lineage

Inspect downstream impact before schema changes:

```bash
python -m src.lakehouse.cli lineage --from-node bronze.raw_orders
```

## Retention

Retention defaults follow layer configuration in `blueprint/lakehouse.yml`:

| Layer | Retention |
|-------|-----------|
| Bronze | 90 days |
| Silver | 365 days |
| Gold | 730 days |

## Change control

1. Update blueprint manifests in a pull request
2. Run `python -m src.lakehouse.cli validate`
3. Review lineage impact for affected nodes
4. Update Terraform or SQL assets if infrastructure changes
5. Document rollback steps in the PR

## Access reviews

- Analyst role must remain gold read-only
- Deploy permissions limited to `data_engineer`
- Re-validate with `tests/test_access.py` after policy changes
