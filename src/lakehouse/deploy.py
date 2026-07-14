"""Deployment and rollback planning."""

from __future__ import annotations

from src.lakehouse.models import DeploymentStep, LakehouseBlueprint


def build_deployment_plan(blueprint: LakehouseBlueprint) -> list[DeploymentStep]:
    steps: list[DeploymentStep] = [
        DeploymentStep(
            order=1,
            action="terraform apply storage module",
            target="bronze/silver/gold buckets",
            rollback="terraform destroy -target=module.storage",
        ),
        DeploymentStep(
            order=2,
            action="terraform apply iam module",
            target="layer-scoped roles",
            rollback="terraform destroy -target=module.iam",
        ),
        DeploymentStep(
            order=3,
            action="terraform apply catalog module",
            target="glue database and layer tables",
            rollback="terraform destroy -target=module.catalog",
        ),
    ]

    order = 4
    for layer in blueprint.layers:
        for table in layer.tables:
            steps.append(
                DeploymentStep(
                    order=order,
                    action=f"create {layer.name} table",
                    target=f"{layer.name}.{table.name}",
                    rollback=f"drop table {layer.name}.{table.name}",
                )
            )
            order += 1

    steps.append(
        DeploymentStep(
            order=order,
            action="validate lineage and access policies",
            target=blueprint.name,
            rollback="revert blueprint commit and re-run validation",
        )
    )
    return steps


def build_rollback_plan(steps: list[DeploymentStep]) -> list[DeploymentStep]:
    return sorted(steps, key=lambda step: step.order, reverse=True)
