"""Blueprint validation orchestration."""

from __future__ import annotations

from pathlib import Path

from src.lakehouse.access import load_access, validate_access
from src.lakehouse.lineage import load_lineage, validate_lineage
from src.lakehouse.manifest import load_lakehouse
from src.lakehouse.models import ValidationIssue
from src.lakehouse.partition import load_partitioning, validate_partitioning


def validate_blueprint(blueprint_dir: Path) -> list[ValidationIssue]:
    blueprint = load_lakehouse(blueprint_dir / "lakehouse.yml")
    partitions = load_partitioning(blueprint_dir / "partitioning.yml")
    roles, _policies = load_access(blueprint_dir / "access.yml")
    nodes, edges, _governance = load_lineage(blueprint_dir / "lineage.yml")

    issues: list[ValidationIssue] = []
    issues.extend(validate_partitioning(blueprint, partitions))
    issues.extend(validate_access(roles))
    issues.extend(validate_lineage(nodes, edges))

    for layer in blueprint.layers:
        for table in layer.tables:
            if table.upstream:
                upstream_layer = table.upstream.split(".", 1)[0]
                layer_order = [entry.name for entry in blueprint.layers]
                if layer_order.index(upstream_layer) >= layer_order.index(layer.name):
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="invalid_layer_flow",
                            message=(
                                f"{table.layer}.{table.name} upstream {table.upstream} "
                                "must come from an earlier layer"
                            ),
                        )
                    )

    return issues
