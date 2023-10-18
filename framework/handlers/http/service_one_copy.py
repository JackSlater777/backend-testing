import requests
from framework.models.services import service_one
from config.auth import auth
from env_vars import APIGW_BASE_URL


class ServiceOneHttpClient:
    service_name = "service-one"

    @staticmethod
    def v1_handler_one(
            body: dict | list | service_one.V1HandlerOneHttpRequest, expected_status: int = 200
    ) -> dict | list | service_one.V1HandlerOneHttpResponse:
        url = "/v1-handler-one"
        response = requests.post(url=APIGW_BASE_URL + url, json=body, headers=auth.get_bearer_token())
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()


# class ServiceOneHttpClient:
#     def __init__(self):
#         self.token = None
#
#     def get_bearer_token(self):
#         if not self.token:
#             self.token = bearer_token.get_bearer_token(payload=payload, headers=headers)
#         return self.token
#
#     @allure.step("service: ServiceOneHttpClient, handler: /v1_handler_one")
#     def v1_handler_one(self, body: dict, expected_status: HTTPStatus):
#         url = "/v1-handler-one"
#         with allure.step("Do request"):
#             response = requests.post(url=APIGW_BASE_URL + url, json=body, headers=self.get_bearer_token())
#         allure.attach(json.dumps(response.json(), ensure_ascii=False, indent=4), 'Response from ServiceOneHttpClient',
#                       allure.attachment_type.JSON)
#         with allure.step(f"Check the status: {response.status_code}"):
#             assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
#         return response
