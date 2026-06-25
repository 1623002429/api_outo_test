from typing import Any

import allure
from jsonpath_ng import parse

from api_auto_test.common.log_util import get_logger


logger = get_logger()


def response_json(response) -> Any:
    if not response.text:
        return None
    return response.json()


def get_by_jsonpath(data: Any, expr: str) -> Any:
    matches = [match.value for match in parse(expr).find(data)]
    if not matches:
        raise AssertionError(f"JSONPath 未匹配到数据：{expr}")
    return matches[0] if len(matches) == 1 else matches


def assert_response(response, checks: list[dict]) -> None:
    body = response_json(response)
    for check in checks or []:
        check_type = check["type"]
        if check_type == "status_code":
            actual = response.status_code
            expected = check["expected"]
            _assert_equal("status_code", "-", expected, actual)
        elif check_type == "json_equal":
            actual = get_by_jsonpath(body, check["path"])
            expected = check["expected"]
            _assert_equal("json_equal", check["path"], expected, actual)
        elif check_type == "json_contains":
            actual = get_by_jsonpath(body, check["path"])
            expected = check["expected"]
            _assert_contains("json_contains", check["path"], expected, actual)
        elif check_type == "text_contains":
            expected = check["expected"]
            _assert_contains("text_contains", "-", expected, response.text)
        elif check_type == "empty_body":
            actual = response.text
            with allure.step(f"断言：响应体为空，预期结果=空，实际结果={_fmt(actual)}"):
                logger.info("断言：类型=响应体为空 字段=- 预期结果=空 实际结果=%s", _fmt(actual))
                assert response.text in ("", "null") or response.content == b"", (
                    f"断言失败：响应体应为空，实际结果={_fmt(actual)}"
                )
                logger.info("断言结果：通过")
        else:
            raise ValueError(f"不支持的断言类型：{check_type}")


def _assert_equal(assert_type: str, path: str, expected: Any, actual: Any) -> None:
    title = f"断言：类型={_assert_name(assert_type)}，字段={path}，预期结果={_fmt(expected)}，实际结果={_fmt(actual)}"
    with allure.step(title):
        logger.info(
            "断言：类型=%s 字段=%s 预期结果=%s 实际结果=%s",
            _assert_name(assert_type),
            path,
            _fmt(expected),
            _fmt(actual),
        )
        assert actual == expected, (
            f"断言失败：字段={path}，预期结果={_fmt(expected)}，实际结果={_fmt(actual)}"
        )
        logger.info("断言结果：通过")


def _assert_contains(assert_type: str, path: str, expected: Any, actual: Any) -> None:
    title = f"断言：类型={_assert_name(assert_type)}，字段={path}，预期包含={_fmt(expected)}，实际结果={_fmt(actual)}"
    with allure.step(title):
        logger.info(
            "断言：类型=%s 字段=%s 预期包含=%s 实际结果=%s",
            _assert_name(assert_type),
            path,
            _fmt(expected),
            _fmt(actual),
        )
        assert expected in actual, (
            f"断言失败：字段={path}，实际结果={_fmt(actual)}，不包含预期结果={_fmt(expected)}"
        )
        logger.info("断言结果：通过")


def _assert_name(assert_type: str) -> str:
    names = {
        "status_code": "状态码等于",
        "json_equal": "JSON字段等于",
        "json_contains": "JSON字段包含",
        "text_contains": "响应文本包含",
        "empty_body": "响应体为空",
    }
    return names.get(assert_type, assert_type)


def _fmt(value: Any) -> str:
    if value == "":
        return "空字符串"
    return repr(value)
