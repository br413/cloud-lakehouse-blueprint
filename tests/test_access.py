from pathlib import Path

from src.lakehouse.access import load_access, validate_access


def test_access_policies_are_safe() -> None:
    roles, _policies = load_access(Path("blueprint/access.yml"))
    issues = validate_access(roles)
    assert issues == []
