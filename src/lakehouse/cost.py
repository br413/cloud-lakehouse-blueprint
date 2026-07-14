"""Cost and performance estimation."""

from __future__ import annotations

from pathlib import Path

import yaml

from src.lakehouse.models import CostEstimate


def load_cost(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def estimate_costs(config: dict[str, object]) -> list[CostEstimate]:
    assumptions = config["assumptions"]
    storage_rate = float(assumptions["storage_cost_per_gb_month"])
    compute_rate = float(assumptions["compute_cost_per_dbu"])
    pruning_savings = float(assumptions["partition_pruning_savings_pct"]) / 100
    z_order_savings = float(assumptions["z_order_savings_pct"]) / 100

    estimates: list[CostEstimate] = []
    for environment, values in config["environments"].items():
        storage_gb = float(values["monthly_storage_gb"])
        compute_dbus = float(values["daily_compute_dbus"]) * 30
        storage_usd = storage_gb * storage_rate
        compute_usd = compute_dbus * compute_rate
        optimized_compute = compute_usd * (1 - pruning_savings - z_order_savings)
        optimized_storage = storage_usd * (1 - (pruning_savings / 2))

        estimates.append(
            CostEstimate(
                environment=environment,
                storage_usd=round(storage_usd, 2),
                compute_usd=round(compute_usd, 2),
                optimized_storage_usd=round(optimized_storage, 2),
                optimized_compute_usd=round(max(optimized_compute, 0), 2),
                notes=(
                    f"partition pruning target: {assumptions['partition_pruning_savings_pct']}%",
                    f"z-order target: {assumptions['z_order_savings_pct']}%",
                ),
            )
        )

    return estimates
