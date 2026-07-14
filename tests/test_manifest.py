from pathlib import Path

from src.lakehouse.manifest import load_lakehouse, table_keys


def test_load_lakehouse_blueprint() -> None:
    blueprint = load_lakehouse(Path("blueprint/lakehouse.yml"))
    assert blueprint.name == "retail-lakehouse"
    assert len(blueprint.layers) == 3
    assert table_keys(blueprint) == {
        "bronze.raw_orders",
        "bronze.raw_customers",
        "silver.stg_orders",
        "silver.dim_customers",
        "gold.fct_daily_orders",
        "gold.rpt_customer_summary",
    }
