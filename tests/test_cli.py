import json
from pathlib import Path

from src.lakehouse.cli import main


def test_validate_json_output_is_parseable(capsys) -> None:
    exit_code = main(["validate", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert isinstance(payload, list)
