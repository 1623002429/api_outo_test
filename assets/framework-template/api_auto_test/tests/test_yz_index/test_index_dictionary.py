import pytest

import allure
from api_auto_test.common.case_runner import run_api_case
from api_auto_test.common.data_loader import load_yaml


index_data = load_yaml("data/yz_index_dictionary.yaml")
cases = index_data["cases"]
case_indexes = list(range(len(cases)))


@allure.epic("DAAS 接口自动化")
@allure.feature("原子指标字典")
@pytest.mark.index
class TestIndexDictionary:
    # @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case_index",
        case_indexes,
        ids=[f"{index + 1:02d}_{case['name']}" for index, case in enumerate(cases)],
    )
    def test_index_dictionary_flow(self, api_client, case_index):
        case = cases[case_index]
        allure.dynamic.title(f"{case_index + 1:02d}. {case['name']}")
        if case.get("skip"):
            pytest.skip(case.get("skip_reason", "该用例在 YAML 中设置为跳过"))
        run_api_case(api_client, index_data["module"], case_index, case)
