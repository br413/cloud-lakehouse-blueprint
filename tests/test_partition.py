from pathlib import Path

from src.lakehouse.manifest import load_lakehouse
from src.lakehouse.partition import load_partitioning, render_partition_ddl, validate_partitioning


def test_partitioning_covers_all_tables() -> None:
    blueprint = load_lakehouse(Path("blueprint/lakehouse.yml"))
    partitions = load_partitioning(Path("blueprint/partitioning.yml"))
    issues = validate_partitioning(blueprint, partitions)
    assert issues == []


def test_render_partition_ddl() -> None:
    partitions = load_partitioning(Path("blueprint/partitioning.yml"))
    ddl = render_partition_ddl(partitions["silver.stg_orders"])
    assert "PARTITIONED BY" in ddl
    assert "updated_at" in ddl
