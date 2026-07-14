"""Load lakehouse blueprint manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.lakehouse.models import LakehouseBlueprint, LayerSpec, TableSpec


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping")
    return value


def load_lakehouse(path: Path) -> LakehouseBlueprint:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    root = _mapping(document, "lakehouse blueprint")

    layers: list[LayerSpec] = []
    for layer_name, layer_data in _mapping(root["layers"], "layers").items():
        layer = _mapping(layer_data, f"layer {layer_name}")
        tables = tuple(
            TableSpec(
                name=table["name"],
                layer=layer_name,
                columns=tuple(table["columns"]),
                upstream=table.get("upstream"),
                source=table.get("source"),
            )
            for table in layer["tables"]
        )
        layers.append(
            LayerSpec(
                name=layer_name,
                description=str(layer.get("description", "")),
                format=str(layer["format"]),
                retention_days=int(layer["retention_days"]),
                tables=tables,
            )
        )

    return LakehouseBlueprint(
        name=str(root["name"]),
        version=str(root["version"]),
        description=str(root.get("description", "")),
        layers=tuple(layers),
    )


def table_keys(blueprint: LakehouseBlueprint) -> set[str]:
    return {f"{table.layer}.{table.name}" for layer in blueprint.layers for table in layer.tables}
