from pathlib import Path

from src.lakehouse.cost import estimate_costs, load_cost


def test_cost_estimates_include_optimization() -> None:
    estimates = estimate_costs(load_cost(Path("blueprint/cost.yml")))
    assert len(estimates) == 2
    prod = next(entry for entry in estimates if entry.environment == "prod")
    assert prod.storage_usd > prod.optimized_storage_usd
    assert prod.compute_usd > prod.optimized_compute_usd
