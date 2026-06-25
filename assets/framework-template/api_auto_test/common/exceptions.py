class ApiTestError(Exception):
    """Base exception for readable API automation failures."""


class ContextVariableMissing(ApiTestError):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name
        super().__init__(f"上下文变量不存在: {variable_name}")


class ApiRequestError(ApiTestError):
    pass

