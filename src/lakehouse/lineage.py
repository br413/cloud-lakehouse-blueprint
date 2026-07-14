"""Lineage and governance helpers."""

from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path

import yaml

from src.lakehouse.models import LineageEdge, ValidationIssue


def load_lineage(path: Path) -> tuple[list[str], list[LineageEdge], dict[str, object]]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    nodes = [node["id"] for node in document["nodes"]]
    edges = [
        LineageEdge(source=edge["from"], target=edge["to"])
        for edge in document["edges"]
    ]
    governance = document.get("governance", {})
    return nodes, edges, governance


def build_adjacency(edges: list[LineageEdge]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        graph[edge.source].append(edge.target)
    return graph


def downstream_nodes(edges: list[LineageEdge], start: str) -> list[str]:
    graph = build_adjacency(edges)
    visited: list[str] = []
    queue = deque(graph.get(start, []))

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.append(node)
        queue.extend(graph.get(node, []))

    return visited


def validate_lineage(nodes: list[str], edges: list[LineageEdge]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    known = set(nodes)

    for edge in edges:
        if edge.source not in known:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="unknown_source",
                    message=f"lineage source {edge.source} is undefined",
                )
            )
        if edge.target not in known:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="unknown_target",
                    message=f"lineage target {edge.target} is undefined",
                )
            )

    return issues
