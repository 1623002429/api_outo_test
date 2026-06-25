"""
Run one YAML case directly for local debugging.

Usage examples:
    python debug_one_case.py
    python debug_one_case.py 创建主题
    python debug_one_case.py 查询创建的主题
"""

import sys

from api_auto_test.common.assert_util import assert_response
from api_auto_test.common.config_loader import load_config
from api_auto_test.common.context import context
from api_auto_test.common.data_loader import load_yaml
from api_auto_test.common.extract_util import extract_to_context
from api_auto_test.common.request_client import RequestClient
from api_auto_test.common.template import render


def find_case(case_name: str | None) -> dict:
    data = load_yaml("data/fh_index_dictionary.yaml")
    cases = data["cases"]
    if not case_name:
        return cases[0]

    for case in cases:
        if case["name"] == case_name:
            return case
    names = "、".join(case["name"] for case in cases)
    raise ValueError(f"未找到用例: {case_name}。可选用例: {names}")


def run_case(case_name: str | None = None) -> None:
    # 调试单条“查询/编辑/删除”这类依赖前置数据的接口时，
    # 需要先跑过前置接口，或手动在 data/runtime_context.json/context 里准备数据。
    config = load_config()
    client = RequestClient(config)
    case = render(find_case(case_name))

    print(f"Running case: {case['name']}")
    response = client.request(
        method=case["method"],
        path=case["path"],
        case_name=case["name"],
        params=case.get("params"),
        json=case.get("json"),
    )

    print("status_code:", response.status_code)
    print("response_text:", response.text)

    assert_response(response, case.get("asserts", []))
    extract_to_context(response, case.get("extract"))

    print("extract_context:", context.all())
    print("debug case passed")


if __name__ == "__main__":
    # name = sys.argv[1] if len(sys.argv) > 1 else None
    # run_case(name)
    if __name__ == "__main__":
        run_case("复合指标创建")