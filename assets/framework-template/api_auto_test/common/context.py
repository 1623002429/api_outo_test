import json
from pathlib import Path
from typing import Any

from api_auto_test.common.config_loader import ROOT_DIR


class Context:
    """保存接口之间需要传递的数据，例如 domainId、_token、domainName。"""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self.data_file = ROOT_DIR / "data" / "runtime_context.json"
        self.load()

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def all(self) -> dict[str, Any]:
        return dict(self._data)

    def clear(self) -> None:
        self._data.clear()
        if self.data_file.exists():
            self.data_file.unlink()

    def load(self) -> None:
        if not self.data_file.exists():
            return
        try:
            self._data.update(json.loads(self.data_file.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            self._data.clear()

    def save(self) -> None:
        self.data_file.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


context = Context()
