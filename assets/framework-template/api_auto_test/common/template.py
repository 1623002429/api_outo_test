import re
from datetime import datetime
from typing import Any

from api_auto_test.common.context import context
from api_auto_test.common.exceptions import ContextVariableMissing


def render(value: Any, variables: dict[str, Any] | None = None) -> Any:
    """渲染 YAML 中的变量：${timestamp}、${ctx.xxx}。"""
    variables = variables or {"timestamp": datetime.now().strftime("%Y%m%d%H%M%S")}
    if isinstance(value, str):
        if value == "${timestamp}":
            return variables["timestamp"]
        value = value.replace("${timestamp}", str(variables["timestamp"]))

        full_ctx_match = re.fullmatch(r"\$\{ctx\.([^}]+)\}", value)
        if full_ctx_match:
            key = full_ctx_match.group(1)
            ctx_value = context.get(key)
            if ctx_value is None:
                raise ContextVariableMissing(key)
            return ctx_value

        def replace_ctx(match: re.Match) -> str:
            key = match.group(1)
            ctx_value = context.get(key)
            if ctx_value is None:
                raise ContextVariableMissing(key)
            return str(ctx_value)

        return re.sub(r"\$\{ctx\.([^}]+)\}", replace_ctx, value)
    if isinstance(value, dict):
        return {k: render(v, variables) for k, v in value.items()}
    if isinstance(value, list):
        return [render(item, variables) for item in value]
    return value
