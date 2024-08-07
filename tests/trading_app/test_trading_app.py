import allure
import pytest
from framework.models.services.trading_app.user import RequestUser, ResponseUser
from framework.utils.pydantic.validator import PydanticValidator
from http import HTTPStatus

# Launch file/class/test separately:
# pytest tests/trading_app/test_trading_app.py::TestV1GetUsersAll:test_200 -s -v --alluredir=output --clean-alluredir

# Launch Allure report on localhost:
# allure serve output


# Кейсы показывают примеры разных запросов - с телом (json), с парамсами (


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
                response_schema=ResponseUser, response=user
            )


@allure.suite("POST /add_user")
class TestV1PostAddUser:
    """
    handler: /add_user
    method: POST
    """
    def test_200(self, trading_app_http_client):
        # body = RequestUser(
        #     role="King",
        #     name="Ivan"
        # )
        body = {
            "role": "King",
            "name": "Ivan"
        }
        response = trading_app_http_client.v1_post_add_user(body=body)
        PydanticValidator.validate_response_schema(
            response_schema=ResponseUser, response=response
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
            response_schema=ResponseUser, response=response
        )

    @pytest.mark.parametrize(
        "value", [123, None]
    )
    def test_400(self, value, trading_app_http_client):
        """Error 400 - validation error"""
        response = trading_app_http_client.v1_patch_change_user_name(
            user_id=1,
            new_name=value,
            expected_status=HTTPStatus.BAD_REQUEST
        )
        # TODO: scheme err400
        # PydanticValidator.validate_response_schema(
        #     response_schema=Error400, response=response
        # )
