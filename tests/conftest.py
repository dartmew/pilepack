import pytest
from pathlib import Path
import shutil

@pytest.fixture
def test_project(tmp_path):
    src = Path(__file__).parent / "fixtures" / "test_project"
    dst = tmp_path / "test_project"
    shutil.copytree(src, dst)
    return dst