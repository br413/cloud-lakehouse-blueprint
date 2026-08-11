# Cost and performance

## Estimation model

Run:

```bash
python -m src.lakehouse.cli cost
```

The model uses configurable assumptions from `blueprint/cost.yml`:

- Storage: $0.023 / GB / month
- Compute: $0.15 / DBU
- Partition pruning savings target: 35%
- Z-order savings target: 15%

## Environment profiles

| Environment | Storage (GB/mo) | Compute (DBU/day) |
|-------------|-----------------|-------------------|
| dev | 120 | 8 |
| prod | 2400 | 64 |

## Performance targets

| Metric | Target |
|--------|--------|
| Gold query p95 | 5 seconds |
| Silver refresh SLA | 30 minutes |
| Bronze landing lag | 10 minutes |

## Optimization levers

1. **Partition pruning** — date partitions on fact tables
2. **Region filters** — dimension tables partitioned by `region`
3. **Layer retention** — shorter bronze retention reduces storage cost
4. **Gold aggregation** — pre-compute daily metrics to limit scan volume

## Review cadence

Re-estimate costs when:

- Table volume grows 2x
- New gold marts are added
- Query concurrency changes

## Example output

```bash
python -m src.lakehouse.cli cost
```

Typical dev vs prod monthly estimates (from default `blueprint/cost.yml`):

| Environment | Storage (USD/mo) | Compute (USD/mo) | Optimized compute (USD/mo) |
|-------------|------------------|------------------|----------------------------|
| dev | ~2.76 | ~36.00 | ~18.00 |
| prod | ~55.20 | ~288.00 | ~144.00 |

Optimized columns apply configured partition-pruning and Z-order savings targets — treat them as planning bounds until validated against real query profiles.

## Operational notes

- Run cost estimates in CI or weekly ops review after manifest changes; see [`docs/operations.md`](operations.md).
- If prod compute optimized estimate exceeds budget, prioritize gold pre-aggregation and bronze retention reduction before scaling warehouse size.
- Keep `assumptions` in `blueprint/cost.yml` under version control so cost discussions reference the same unit rates as the CLI.
