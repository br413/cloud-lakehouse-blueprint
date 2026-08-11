# Operations runbook

Day-2 operations for a manifest-driven lakehouse blueprint — validation, cost review, access changes, and recovery.

## Daily checks

| Check | Command / signal | Action if failing |
|-------|------------------|-------------------|
| Blueprint valid | `python -m src.lakehouse.cli validate` | Fix manifest YAML before any deploy |
| Partition coverage | Review `blueprint/partitioning.yml` vs new tables | Add partition keys before prod data lands |
| Access drift | `python -m src.lakehouse.cli validate` (access rules) | Block deploy until IAM policies match manifest |
| Cost estimate | `python -m src.lakehouse.cli cost` | Compare to budget; tune `blueprint/cost.yml` assumptions |

## Cost review workflow

1. Run `python -m src.lakehouse.cli cost` after changing table volume or environment profiles in `blueprint/cost.yml`.
2. Compare **dev** vs **prod** monthly storage and compute lines — prod should reflect realistic bronze retention and gold query concurrency.
3. Re-estimate when any trigger in [`docs/cost-performance.md`](cost-performance.md#review-cadence) applies (2x volume, new marts, concurrency change).
4. Track optimized vs baseline compute — partition pruning and Z-order savings are targets; validate with query metrics in your warehouse before treating them as realized savings.

## Deployment and rollback

See [`docs/deployment.md`](deployment.md) for the full sequence. Summary:

1. `validate` → `plan` → review Terraform diff
2. Apply storage module before catalog/IAM role changes that reference bucket paths
3. Rollback: run generated plan steps in **reverse order**; do not delete bronze buckets without archival confirmation

## Incident response

### Validation fails in CI

**Symptoms:** GitHub Actions `validate` job red; merge blocked.

**Steps:**

1. Run locally: `python -m src.lakehouse.cli validate --json`
2. Fix manifest errors (missing lineage target, invalid access role, partition mismatch)
3. Re-run `pytest` and push fix

### Unexpected IAM access denial

**Symptoms:** Consumer role cannot read silver/gold paths after deploy.

**Steps:**

1. Compare `blueprint/access.yml` with Terraform IAM module output
2. Confirm layer prefix in S3 matches manifest table locations
3. Re-apply IAM module only after manifest fix is merged

### Cost spike after new gold mart

**Symptoms:** `cost` CLI shows prod compute jump; p95 gold queries exceed target in [`docs/cost-performance.md`](cost-performance.md).

**Steps:**

1. Confirm new mart is aggregated (daily rollups) not raw fact scans
2. Add or tighten date partitions on upstream silver tables
3. Update `blueprint/cost.yml` prod `daily_compute_dbus` to reflect measured usage

## Monitoring suggestions (when deployed)

| Signal | Source | Alert threshold |
|--------|--------|-----------------|
| Bronze landing lag | Orchestrator task duration | > 10 minutes (see cost-performance SLA) |
| Silver refresh duration | Job metrics | > 30 minutes |
| Gold query p95 | Warehouse query history | > 5 seconds |
| Storage growth | S3 inventory / cloud billing | > 2x baseline month-over-month |

## Ownership

| Area | Owner |
|------|-------|
| Manifest changes | Data platform / architect |
| Terraform apply | Platform engineer |
| Cost assumptions | FinOps + data platform (monthly) |
| Access policy updates | Security + data steward |
