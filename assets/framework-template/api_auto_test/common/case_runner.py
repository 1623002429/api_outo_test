import allure

from api_auto_test.common.assert_util import assert_response
from api_auto_test.common.context import context
from api_auto_test.common.exceptions import ApiTestError, ContextVariableMissing
from api_auto_test.common.extract_util import extract_to_context
from api_auto_test.common.log_util import get_logger
from api_auto_test.common.template import render


logger = get_logger()


def run_api_case(api_client, module_name: str, case_index: int, case: dict):
    case_name = case.get("name", f"case_{case_index + 1}")
    case_title = f"{module_name} / {case_index + 1:02d}. {case_name}"
    _set_allure_module_labels(module_name, case_index, case_name)

    try:
        rendered_case = render(case)
        with allure.step(rendered_case["name"]):
            response = api_client.request(
                method=rendered_case["method"],
                path=rendered_case["path"],
                case_name=case_title,
                params=rendered_case.get("params"),
                json=rendered_case.get("json"),
                data=rendered_case.get("data"),
            )
            assert_response(response, rendered_case.get("asserts", []))
            extract_to_context(response, rendered_case.get("extract"))
    except ContextVariableMissing as exc:
        message = (
            f"上下文变量缺失 | 模块={module_name} | 用例={case_index + 1:02d}. {case_name} | "
            f"缺失变量={exc.variable_name} | 当前上下文={context.all()} | "
            "常见原因：前置接口失败、超时、被跳过，或 extract 没有提取到该变量。"
        )
        logger.error(message)
        allure.attach(message, "context-variable-missing", allure.attachment_type.TEXT)
        raise AssertionError(message) from exc
    except ApiTestError:
        raise
    except AssertionError:
        raise
    except Exception as exc:
        message = (
            f"用例执行异常 | 模块={module_name} | 用例={case_index + 1:02d}. {case_name} | "
            f"错误类型={type(exc).__name__} | 错误信息={exc}"
        )
        logger.error(message)
        allure.attach(message, "case-error", allure.attachment_type.TEXT)
        raise AssertionError(message) from exc


def _set_allure_module_labels(module_name: str, case_index: int, case_name: str) -> None:
    """Use YAML module/case names for Allure grouping instead of Python package names."""
    allure.dynamic.epic("DAAS 接口自动化")
    allure.dynamic.feature(module_name)
    allure.dynamic.story(case_name)
    allure.dynamic.parent_suite("接口自动化")
    allure.dynamic.suite(module_name)
    allure.dynamic.sub_suite(f"{case_index + 1:02d}. {case_name}")
