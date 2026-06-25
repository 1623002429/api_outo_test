from pathlib import Path
import os
import re
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT_DIR / "config" / "config.yaml"


def _replace_env(value: Any) -> Any:
    """把配置里的 ${ENV_NAME} 替换为环境变量值。"""
    if isinstance(value, str):
        pattern = re.compile(r"\$\{([^}]+)\}")
        return pattern.sub(lambda m: os.getenv(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _replace_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_replace_env(item) for item in value]
    return value


def load_config() -> dict:
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    env = raw.get("env", "test")
    config = raw[env]
    config["env"] = env
    return _replace_env(config)
