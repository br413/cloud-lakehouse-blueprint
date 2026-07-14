from pathlib import Path

import pytest

from src.lakehouse.manifest import load_lakehouse

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "blueprint"


@pytest.fixture
def blueprint():
    return load_lakehouse(BLUEPRINT / "lakehouse.yml")
