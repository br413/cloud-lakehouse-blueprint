"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.lakehouse.access import load_access
from src.lakehouse.cost import estimate_costs, load_cost
from src.lakehouse.deploy import build_deployment_plan, build_rollback_plan
from src.lakehouse.lineage import downstream_nodes, load_lineage
from src.lakehouse.manifest import load_lakehouse
from src.lakehouse.partition import load_partitioning, render_partition_ddl
from src.lakehouse.validator import validate_blueprint


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and plan a cloud lakehouse blueprint")
    parser.add_argument("--blueprint-dir", type=Path, default=Path("blueprint"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="Validate blueprint manifests")
    subparsers.add_parser("plan", help="Render deployment and rollback plans")

    cost_parser = subparsers.add_parser("cost", help="Estimate storage and compute costs")
    cost_parser.add_argument("--environment", default=None)

    lineage_parser = subparsers.add_parser("lineage", help="Show downstream lineage")
    lineage_parser.add_argument("--from-node", required=True)

    ddl_parser = subparsers.add_parser("ddl", help="Render partition DDL")
    ddl_parser.add_argument("--table", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    blueprint_dir: Path = args.blueprint_dir

    if args.command == "validate":
        issues = validate_blueprint(blueprint_dir)
        for issue in issues:
            print(f"{issue.severity.upper():7} {issue.code}: {issue.message}")
        return 1 if any(issue.severity == "error" for issue in issues) else 0

    if args.command == "plan":
        blueprint = load_lakehouse(blueprint_dir / "lakehouse.yml")
        deploy_steps = build_deployment_plan(blueprint)
        rollback_steps = build_rollback_plan(deploy_steps)
        print("Deployment plan:")
        for step in deploy_steps:
            print(f"  {step.order}. {step.action} -> {step.target}")
        print("\nRollback plan:")
        for step in rollback_steps:
            print(f"  {step.order}. {step.rollback} ({step.target})")
        return 0

    if args.command == "cost":
        estimates = estimate_costs(load_cost(blueprint_dir / "cost.yml"))
        if args.environment:
            estimates = [entry for entry in estimates if entry.environment == args.environment]
        print(json.dumps([entry.__dict__ for entry in estimates], indent=2))
        return 0

    if args.command == "lineage":
        _nodes, edges, governance = load_lineage(blueprint_dir / "lineage.yml")
        downstream = downstream_nodes(edges, args.from_node)
        print(json.dumps({"from": args.from_node, "downstream": downstream, "governance": governance}, indent=2))
        return 0

    if args.command == "ddl":
        partitions = load_partitioning(blueprint_dir / "partitioning.yml")
        if args.table not in partitions:
            parser.error(f"unknown table: {args.table}")
        print(render_partition_ddl(partitions[args.table]))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
