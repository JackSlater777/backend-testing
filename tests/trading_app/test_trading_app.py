import allure
from framework.models.services.trading_app.user import User
from framework.utils.pydantic.validator import PydanticValidator

# Запуск отдельного файла/класса/теста
# pytest tests/trading_app/test_trading_app.py::TestV1GetUsersAll:test_200 -s -v --alluredir=output --clean-alluredir

# Просмотр отчета на локальном сервере
# allure serve output


@allure.suite("Get /users/all")
class TestV1GetUsersAll:
    """
    handler: /users/all
    method: GET
    """
    def test_200(self, trading_app_http_client):
        response = trading_app_http_client.v1_get_users_all()
        for user in response:
            PydanticValidator.validate_response_schema(
                response_schema=User, response=user
            )


@allure.suite("POST /add_user")
class TestV1PostAddUser:
    """
    handler: /add_user
    method: POST
    """
    def test_200(self, trading_app_http_client):
        response = trading_app_http_client.v1_post_add_user(role="King", name="Ivan")
        PydanticValidator.validate_response_schema(
            response_schema=User, response=response
        )


@allure.suite("PATCH /users/{user_id}")
class TestV1PatchChangeUserName:
    """
    handler: /users/{user_id}
    method: PATCH
    """
    def test_200(self, trading_app_http_client):
        response = trading_app_http_client.v1_patch_change_user_name(
            user_id=1,
            new_name="Ivan"
        )
        PydanticValidator.validate_response_schema(
            response_schema=User, response=response
        )

    # @pytest.mark.parametrize(
    #     "field", [
    #         "field_one",
    #         "field_two",
    #         "field_three"
    #     ]
    # )
    # def test_400_validation(self, field, v1_handler_one_body):
    #     """Error 400 - validation error"""
    #     v1_handler_one_body[field] = None
    #     ServiceOneHttpClient.v1_handler_one(
    #         body=v1_handler_one_body,
    #         expected_status=HTTPStatus.BAD_REQUEST
    #     )
