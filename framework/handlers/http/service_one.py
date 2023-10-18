import requests
from config.auth import auth
from config.config import get_credentials_for_token
from config import configuration


SERVICE_ONE_BASE_URL = configuration.get("team.service_one.address")


class ServiceOneHttpClient:
    service_name = "service-one"

    @staticmethod
    def auth() -> dict:
        url = "/auth"
        # headers = "Content-Type: application/json"
        response = requests.post(url=SERVICE_ONE_BASE_URL + url, json=get_credentials_for_token())
        return response.json()

    # @staticmethod
    # def v1_handler_one(
    #         body: dict | list, expected_status: int = 200
    # ) -> dict | list:
    #     url = "/v1-handler-one"
    #     response = requests.post(url=SERVICE_ONE_BASE_URL + url, json=body, headers=auth.get_bearer_token())
    #     assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
    #     return response.json()
