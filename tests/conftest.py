from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root_dir() -> Path:
    return Path(__file__).resolve().parent.parent
