from pathlib import Path

from src.lakehouse.validator import validate_blueprint


def test_validate_blueprint_passes() -> None:
    issues = validate_blueprint(Path("blueprint"))
    assert [issue for issue in issues if issue.severity == "error"] == []
