# Contributing

## Workflow

1. Open or select an issue.
2. Discuss significant design changes before implementation.
3. Create a focused branch.
4. Add or update tests.
5. Run `pytest` and `terraform validate`.
6. Open a pull request with technical context and validation evidence.

## Commit guidance

```text
feat: add gold layer partitioning strategy
fix: block analyst write permissions in validator
docs: document rollback procedure
test: cover downstream lineage traversal
```

Preserve accurate authorship.

## Pull-request standard

Explain problem, approach, alternatives, testing, operational impact, and rollback strategy when relevant.
