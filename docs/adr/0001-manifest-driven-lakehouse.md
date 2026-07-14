# ADR 0001: Manifest-driven lakehouse blueprint

## Status

Accepted

## Context

Lakehouse projects often split architecture docs, IaC, access policies, and lineage across multiple systems. That makes reviews slow and rollbacks error-prone.

## Decision

Use version-controlled YAML manifests as the source of truth. Validate manifests in CI, generate deployment/rollback plans, and map Terraform modules to medallion layers.

## Consequences

**Positive**

- Single review surface for architecture changes
- Validation runs without cloud credentials
- Clear mapping from blueprint to infrastructure

**Negative**

- Manifests must stay synchronized with Terraform and SQL assets
- AWS-specific Terraform modules require adaptation for other clouds

## Alternatives considered

- **Docs-only architecture** — easy to write, hard to enforce
- **Full Databricks/Snowflake provisioning in CI** — requires credentials and increases CI cost
