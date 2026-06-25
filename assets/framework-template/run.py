import pytest
from pathlib import Path
import os


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent / "api_auto_test"
    os.chdir(project_dir)
    raise SystemExit(pytest.main(["-s", "-v"]))
