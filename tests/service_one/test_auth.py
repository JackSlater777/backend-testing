from framework.handlers.http.service_one import ServiceOneHttpClient


# Запуск отдельного теста/класса/файла/папки
# pytest -s tests/service_one/test_auth.py::TestAuth::test_200 --alluredir=output --clean-alluredir

# Просмотр отчета на локальном сервере
# allure serve output


class TestAuth:
    """
    Tests for:
    service: service_one
    handler: /v1_handler_one
    """
    def test_200(self):
        response = ServiceOneHttpClient.auth()
        print(5)
        # PydanticValidator.validate_response_schema(
        #     response_schema=service_one.V1HandlerOneHttpResponse, response=response
        # )
