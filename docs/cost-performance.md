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
