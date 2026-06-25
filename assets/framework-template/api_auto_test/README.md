# 接口自动化测试框架

基于 `requests + pytest + allure + log + 断言` 搭建，已按 Excel 中的“主题管理”接口链路生成示例用例。

## 目录说明

- `config/config.yaml`：环境、域名、headers、超时等配置。
- `data/topic_domain.yaml`：主题管理模块测试数据。
- `common/request_client.py`：统一请求封装，自动写日志并附加 Allure 请求/响应。
- `common/context.py`：上下接口关联数据保存，例如 `domainId`、`_token`、`domainName`。
- `common/assert_util.py`：状态码、JSONPath、文本、空响应断言。
- `tests/test_topic/test_topic_domain.py`：主题管理测试用例。
- `logs/api_test.log`：运行日志。
- `reports/allure-results`：Allure 原始结果。
- `reports/allure-report`：Allure HTML 报告。

## 安装依赖

```powershell
pip install -r requirements.txt
```

Allure 报告需要本机安装 Allure 命令行工具，并配置到 `PATH`。

## 配置鉴权

建议把真实鉴权信息放到环境变量，避免写死在代码里：

```powershell
$env:DAAS_AUTHORIZATION="Bearer 你的token"
```

如果你原来的 `DAAS.T_headers.headers` 里不是 `Authorization`，可以直接修改 `config/config.yaml` 的 `headers`。

## 执行测试

```powershell
pytest
```

只执行主题管理：

```powershell
pytest -m topic
```

按关键字执行：

```powershell
pytest -k 创建主题
```

生成 Allure 报告：

```powershell
allure generate reports/allure-results -o reports/allure-report --clean
```

临时打开报告：

```powershell
allure serve reports/allure-results
```

也可以使用脚本：

```powershell
.\scripts\run_tests.ps1
.\scripts\run_tests.ps1 -Keyword topic -ServeReport
```

## 上下接口关联

在 YAML 的 `extract` 中配置 JSONPath，把响应字段保存到上下文：

```yaml
extract:
  domain_id: $.domainId
  domain_name: $.domainName
```

后续接口用 `${ctx.domain_id}`、`${ctx.domain_name}` 引用：

```yaml
json:
  parentId: ${ctx.domain_id}
  parentName: ${ctx.domain_name}
```

运行时数据会保存到 `data/runtime_context.json`，方便排查。

## 跳过用例

在数据文件中设置：

```yaml
skip: true
skip_reason: 暂未联调完成
```

## 新增模块

1. 在 `data/` 下新建模块 YAML，例如 `data/user.yaml`。
2. 在 `tests/` 下新建测试文件，例如 `tests/test_user/test_user.py`。
3. 复用 `api_client`、`render`、`assert_response`、`extract_to_context` 即可。
