from pathlib import Path
from typing import Any

import yaml

from api_auto_test.common.config_loader import ROOT_DIR


def load_yaml(relative_path: str) -> Any:
    file_path = ROOT_DIR / relative_path
    with file_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
