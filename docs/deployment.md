# Deployment and rollback

## Prerequisites

- Terraform >= 1.5
- AWS credentials with permission to create S3, IAM, and Glue resources
- Validated blueprint: `python -m src.lakehouse.cli validate`

## Deployment sequence

Generate the plan:

```bash
python -m src.lakehouse.cli plan
```

Expected order:

1. Apply storage module (bronze/silver/gold buckets)
2. Apply IAM module (layer-scoped roles)
3. Apply catalog module (Glue database and layer tables)
4. Create layer tables from `sql/` assets
5. Validate lineage and access policies

### Terraform apply

```bash
cd terraform
terraform init
terraform plan -var="environment=dev"
terraform apply -var="environment=dev"
```

## Rollback

Rollback follows the reverse order from the CLI plan:

1. Revert blueprint commit if validation rules changed
2. Drop newly created tables
3. `terraform destroy -target=module.catalog`
4. `terraform destroy -target=module.iam`
5. `terraform destroy -target=module.storage`

### Partial rollback

If only gold layer deployment fails:

- Roll back gold tables and SQL assets
- Leave bronze/silver intact to avoid re-ingestion
- Re-run `python -m src.lakehouse.cli validate` before retry

## Verification checklist

- [ ] `pytest` passes
- [ ] `terraform validate` passes
- [ ] `python -m src.lakehouse.cli validate` returns exit code 0
- [ ] IAM policies match `blueprint/access.yml`
- [ ] Lineage graph includes all new tables
