from typing import Any

import allure

from api_auto_test.common.assert_util import get_by_jsonpath, response_json
from api_auto_test.common.context import context
from api_auto_test.common.log_util import get_logger


logger = get_logger()


def extract_to_context(response, extract_rules: dict[str, str] | None) -> None:
    """按 JSONPath 提取响应数据并保存到上下文，供后续接口使用。"""
    if not extract_rules:
        return
    body: Any = response_json(response)
    for key, jsonpath_expr in extract_rules.items():
        value = get_by_jsonpath(body, jsonpath_expr)
        with allure.step(f"提取：变量={key}，JSONPath={jsonpath_expr}，提取结果={repr(value)}"):
            logger.info("提取：变量=%s JSONPath=%s 提取结果=%s", key, jsonpath_expr, repr(value))
            context.set(key, value)
    context.save()
