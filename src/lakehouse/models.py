"""Shared domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TableSpec:
    name: str
    layer: str
    columns: tuple[str, ...]
    upstream: str | None = None
    source: str | None = None


@dataclass(frozen=True)
class LayerSpec:
    name: str
    description: str
    format: str
    retention_days: int
    tables: tuple[TableSpec, ...]


@dataclass(frozen=True)
class LakehouseBlueprint:
    name: str
    version: str
    description: str
    layers: tuple[LayerSpec, ...]


@dataclass(frozen=True)
class PartitionSpec:
    table_key: str
    strategy: str
    columns: tuple[str, ...]
    granularity: str


@dataclass(frozen=True)
class RoleSpec:
    name: str
    description: str
    layers: tuple[str, ...]
    permissions: tuple[str, ...]


@dataclass(frozen=True)
class LineageEdge:
    source: str
    target: str


@dataclass(frozen=True)
class CostEstimate:
    environment: str
    storage_usd: float
    compute_usd: float
    optimized_storage_usd: float
    optimized_compute_usd: float
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DeploymentStep:
    order: int
    action: str
    target: str
    rollback: str


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)
