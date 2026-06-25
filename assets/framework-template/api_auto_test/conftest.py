import pytest
import json
import os
import shutil
import subprocess

from api_auto_test.common.config_loader import load_config
from api_auto_test.common.config_loader import ROOT_DIR
from api_auto_test.common.context import context
from api_auto_test.common.log_util import get_logger
from api_auto_test.common.request_client import RequestClient


logger = get_logger()


@pytest.fixture(scope="session")
def config() -> dict:
    return load_config()


@pytest.fixture(scope="session")
def api_client(config) -> RequestClient:
    return RequestClient(config)


@pytest.fixture(scope="session", autouse=True)
def clean_runtime_context():
    # 每次执行前清空历史关联数据，避免上一次测试结果污染本次运行。
    context.clear()
    yield
    context.save()


def pytest_sessionfinish(session, exitstatus):
    """pytest 执行结束后自动生成 Allure HTML 报告。"""
    if session.config.option.collectonly:
        return

    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        logger.warning("Allure command not found, skip HTML report generation.")
        return

    env = os.environ.copy()
    java_home = env.get("JAVA_HOME", "")
    if not java_home or not os.path.exists(os.path.join(java_home, "bin", "java.exe")):
        for candidate in (
            r"C:\Program Files\Java\jdk-25",
            r"C:\Program Files\Java\jdk1.8.0_261",
            r"C:\Program Files\Java\jre1.8.0_261",
        ):
            if os.path.exists(os.path.join(candidate, "bin", "java.exe")):
                env["JAVA_HOME"] = candidate
                env["Path"] = os.path.join(candidate, "bin") + os.pathsep + env.get("Path", "")
                break

    results_dir = ROOT_DIR / "reports" / "allure-results"
    report_dir = ROOT_DIR / "reports" / "allure-report"
    _clean_allure_parameters(results_dir)
    command = [
        allure_cmd,
        "generate",
        str(results_dir),
        "-o",
        str(report_dir),
        "--clean",
    ]

    logger.info("Generating Allure report: %s", " ".join(command))
    completed = subprocess.run(command, cwd=ROOT_DIR, env=env, capture_output=True, text=True)
    if completed.returncode == 0:
        logger.info("Allure report generated: %s", report_dir)
    else:
        logger.error("Allure report generation failed: %s", completed.stderr or completed.stdout)


def _clean_allure_parameters(results_dir):
    """Remove long pytest parameters from Allure result files before report generation."""
    for result_file in results_dir.glob("*-result.json"):
        try:
            data = json.loads(result_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.pop("parameters", None) is not None:
            result_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    for container_file in results_dir.glob("*-container.json"):
        try:
            data = json.loads(container_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        original_befores = data.get("befores", [])
        data["befores"] = [
            item for item in original_befores
            if item.get("name") not in {"case", "case_index"}
        ]
        if data["befores"] != original_befores:
            container_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
