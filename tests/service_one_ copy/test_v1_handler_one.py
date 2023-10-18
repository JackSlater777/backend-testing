import pytest
from http import HTTPStatus
from framework.handlers.http.service_one import ServiceOneHttpClient
from framework.models.services import service_one
from framework.utils.pydantic.validator import PydanticValidator

# Запуск отдельного класса/теста
# pytest tests/service_one/test_v1_handler_one.py::TestCurrentPrice:test_day_200 -s -v --alluredir=output --clean-alluredir

# Запуск всех тестов модуля
# pytest tests/service_one/test_current_price.py -s -v --alluredir=output --clean-alluredir

# Запуск всех тестов папки
# pytest tests/service_one -s -v --alluredir=output --clean-alluredir

# Просмотр отчета на локальном сервере
# allure serve output


class TestV1HandlerOne:
    """
    Tests for:
    service: service_one
    handler: /v1_handler_one
    """
    def test_200(self, mock_service_two_v1_handler_one_day, v1_handler_one_body):
        response = ServiceOneHttpClient.v1_handler_one(body=v1_handler_one_body)
        PydanticValidator.validate_response_schema(
            response_schema=service_one.V1HandlerOneHttpResponse, response=response
        )

    @pytest.mark.parametrize(
        "field", [
            "field_one",
            "field_two",
            "field_three"
        ]
    )
    def test_400_validation(self, field, v1_handler_one_body):
        """Error 400 from price-calc (validation error)"""
        v1_handler_one_body[field] = None
        ServiceOneHttpClient.v1_handler_one(
            body=v1_handler_one_body,
            expected_status=HTTPStatus.BAD_REQUEST
        )


if __name__ == '__main__':
    pytest.main()
