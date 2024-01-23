import requests
# from config.auth import auth
# from config.setup_config import get_credentials_for_token
from config import configuration


class TradingAppHttpClient:
    def __init__(self):
        self.service_name = "trading_app"
        self.url = configuration.get("trading_app").get("address")

    # def auth(self) -> dict:
    #     url = "/auth"
    #     # headers = "Content-Type: application/json"
    #     response = requests.post(url=SERVICE_ONE_BASE_URL + url, json=get_credentials_for_token())
    #     return response.json()

    def v1_get_users_all(self, expected_status: int = 200) -> list:
        handler = "/users/all"
        response = requests.get(url=self.url + handler)
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()

    def v1_post_add_user(self, role: str, name: str, degree: list | None = None, expected_status: int = 200) -> list:
        handler = "/add_user"
        body = {
            "role": role,
            "name": name,
            "degree": degree
        }
        response = requests.post(url=self.url + handler, json=body)
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()

    def v1_patch_change_user_name(self, user_id: int, new_name: str, expected_status: int = 200) -> dict:
        handler = f"/users/{user_id}"
        body = {
            "user_id": user_id,
            "new_name": new_name
        }
        response = requests.patch(url=self.url + handler, params=body)  # /users/1?user_id=1&new_name=Ivan
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()


    # def v1_handler_one(self, body: dict | list, expected_status: int = 200) -> dict | list:
    #     #     handler = "/v1-handler-one"
    #     #     response = requests.post(url=self.url + handler, json=body, headers=auth.get_bearer_token())
    #     #     assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
    #     #     return response.json()
