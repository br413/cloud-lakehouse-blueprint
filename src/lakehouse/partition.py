"""Partitioning strategy helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.lakehouse.manifest import load_lakehouse, table_keys
from src.lakehouse.models import LakehouseBlueprint, PartitionSpec, ValidationIssue


def load_partitioning(path: Path) -> dict[str, PartitionSpec]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    tables = document["tables"]
    return {
        table_key: PartitionSpec(
            table_key=table_key,
            strategy=str(spec["strategy"]),
            columns=tuple(spec["columns"]),
            granularity=str(spec["granularity"]),
        )
        for table_key, spec in tables.items()
    }


def validate_partitioning(
    blueprint: LakehouseBlueprint,
    partitions: dict[str, PartitionSpec],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    known_tables = table_keys(blueprint)

    for table_key in partitions:
        if table_key not in known_tables:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="unknown_table",
                    message=f"partition config references unknown table {table_key}",
                )
            )

    for table_key in sorted(known_tables):
        if table_key not in partitions:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="missing_partition",
                    message=f"no partition strategy for {table_key}",
                )
            )
            continue

        spec = partitions[table_key]
        layer, table_name = table_key.split(".", 1)
        table = next(
            candidate
            for candidate_layer in blueprint.layers
            if candidate_layer.name == layer
            for candidate in candidate_layer.tables
            if candidate.name == table_name
        )
        for column in spec.columns:
            if column not in table.columns:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_partition_column",
                        message=f"{table_key} partition column {column} not in schema",
                    )
                )

    return issues


def render_partition_ddl(spec: PartitionSpec) -> str:
    columns = ", ".join(spec.columns)
    if spec.strategy == "date" and spec.granularity == "day":
        return (
            f"-- {spec.table_key}\n"
            f"PARTITIONED BY (date({spec.columns[0]}) AS {spec.columns[0]}_day)"
        )
    return f"-- {spec.table_key}\nPARTITIONED BY ({columns})"
