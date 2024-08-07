import requests
from framework.models.services.trading_app.user import RequestUser, ResponseUser
from http import HTTPStatus


class TradingAppHttpClient:
    def __init__(self, url, token):
        self.service_name = "trading_app"
        self.url = url
        self.token = token

    def v1_get_users_all(self, expected_status: int = HTTPStatus.OK) -> list[ResponseUser]:
        handler = "/users/all"
        response = requests.get(url=self.url + handler, headers=self.token)
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()

    def v1_post_add_user(self, body: RequestUser, expected_status: int = HTTPStatus.OK) -> list[ResponseUser]:
        handler = "/add_user"
        assert RequestUser.model_validate(body)
        response = requests.post(url=self.url + handler, json=body, headers=self.token)
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()

    def v1_patch_change_user_name(self, user_id: int, new_name: str, expected_status: int = HTTPStatus.OK) -> dict:
        handler = f"/users/{user_id}"
        body = {
            "user_id": user_id,
            "new_name": new_name
        }
        response = requests.patch(url=self.url + handler, params=body, headers=self.token)  # /users/1?user_id=1&new_name=Ivan  # noqa
        assert response.status_code == expected_status, f"Unexpected status received: {response.status_code}"
        return response.json()
