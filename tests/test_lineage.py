from pathlib import Path

from src.lakehouse.lineage import downstream_nodes, load_lineage, validate_lineage


def test_lineage_graph_is_valid() -> None:
    nodes, edges, governance = load_lineage(Path("blueprint/lineage.yml"))
    assert validate_lineage(nodes, edges) == []
    assert governance["owner"] == "data-platform"


def test_downstream_from_bronze_orders() -> None:
    _nodes, edges, _governance = load_lineage(Path("blueprint/lineage.yml"))
    downstream = downstream_nodes(edges, "bronze.raw_orders")
    assert "silver.stg_orders" in downstream
    assert "gold.fct_daily_orders" in downstream
    assert "bi_dashboard" in downstream
