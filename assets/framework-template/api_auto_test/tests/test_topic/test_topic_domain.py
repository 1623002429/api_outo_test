import pytest

import allure
from api_auto_test.common.case_runner import run_api_case
from api_auto_test.common.data_loader import load_yaml


topic_data = load_yaml("data/topic_domain.yaml")
cases = topic_data["cases"]
case_indexes = list(range(len(cases)))


@allure.epic("DAAS 接口自动化")
@allure.feature("主题管理")
@pytest.mark.topic
class TestTopicDomain:
    # @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case_index",
        case_indexes,
        ids=[f"{index + 1:02d}_{case['name']}" for index, case in enumerate(cases)],
    )
    def test_topic_domain_flow(self, api_client, case_index):
        """主题管理主流程：创建、查询、编辑、创建子主题、删除。"""
        case = cases[case_index]
        allure.dynamic.title(f"{case_index + 1:02d}. {case['name']}")
        if case.get("skip"):
            pytest.skip(case.get("skip_reason", "该用例在 YAML 中设置为跳过"))
        run_api_case(api_client, topic_data["module"], case_index, case)
