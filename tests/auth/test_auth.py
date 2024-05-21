import allure
from config.setup_config import get_credentials_for_bearer_token


@allure.suite("Get /users/all")
class TestGetBearerToken:
    """
    handler: /auth/realms/APIGW_API/protocol/openid-connect/token
    method: POST
    """
    def test_200(self, auth_http_client):
        token = auth_http_client.get_bearer_token(payload=get_credentials_for_bearer_token())
        print(token)
