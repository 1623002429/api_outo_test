import json
from urllib.parse import urljoin

import allure
import requests

from api_auto_test.common.exceptions import ApiRequestError
from api_auto_test.common.log_util import get_logger


class RequestClient:
    def __init__(self, config: dict):
        self.base_url = config["base_url"].rstrip("/")
        self.timeout = config.get("timeout", 20)
        self.verify_ssl = config.get("verify_ssl", True)
        self.session = requests.Session()
        self.session.headers.update({k: v for k, v in config.get("headers", {}).items() if v})
        self.logger = get_logger()

    def request(self, method: str, path: str, case_name: str | None = None, **kwargs) -> requests.Response:
        url = path if path.startswith("http") else urljoin(f"{self.base_url}/", path.lstrip("/"))
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", self.verify_ssl)

        title = f"{case_name} - {method.upper()} {url}" if case_name else f"{method.upper()} {url}"
        with allure.step(title):
            self.logger.info("=" * 100)
            self.logger.info("Case: %s", case_name or "-")
            self.logger.info("Request: %s %s", method.upper(), url)
            self.logger.info("Params: %s", self._to_json(kwargs.get("params")))
            self.logger.info("Body: %s", self._to_json(kwargs.get("json") or kwargs.get("data")))
            try:
                response = self.session.request(method=method.upper(), url=url, **kwargs)
            except requests.exceptions.Timeout as exc:
                message = (
                    f"接口请求超时 | 用例={case_name or '-'} | "
                    f"请求={method.upper()} {url} | timeout={kwargs.get('timeout')} | "
                    f"params={self._to_json(kwargs.get('params'))} | "
                    f"body={self._to_json(kwargs.get('json') or kwargs.get('data'))} | "
                    f"原始错误={exc}"
                )
                self.logger.error(message)
                allure.attach(message, "request-timeout", allure.attachment_type.TEXT)
                raise ApiRequestError(message) from exc
            except requests.exceptions.RequestException as exc:
                message = (
                    f"接口请求失败 | 用例={case_name or '-'} | "
                    f"请求={method.upper()} {url} | "
                    f"params={self._to_json(kwargs.get('params'))} | "
                    f"body={self._to_json(kwargs.get('json') or kwargs.get('data'))} | "
                    f"原始错误={exc}"
                )
                self.logger.error(message)
                allure.attach(message, "request-error", allure.attachment_type.TEXT)
                raise ApiRequestError(message) from exc
            self.logger.info("Response status: %s", response.status_code)
            self.logger.info("Response body: %s", response.text)
            self.logger.info("=" * 100)
            allure.attach(self._to_json({k: v for k, v in kwargs.items() if k != "verify"}), "request", allure.attachment_type.TEXT)
            allure.attach(response.text or "", "response", allure.attachment_type.TEXT)
            return response

    @staticmethod
    def _to_json(value) -> str:
        if value is None:
            return "{}"
        try:
            return json.dumps(value, ensure_ascii=False, indent=2)
        except TypeError:
            return str(value)
