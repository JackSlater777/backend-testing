import requests
from http import HTTPStatus
from config import configuration


class Token:
    def __init__(self):
        self.url = configuration.get("fsso").get("address")

    def get_bearer_token(self, payload: str):
        """Get a bearer_token token"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = "/auth/realms/APIGW_API/protocol/openid-connect/token"
        response = requests.post(url=self.url+url, headers=headers, data=payload)
        assert response.status_code == HTTPStatus.OK, f"Unexpected status received: {response.status_code}"
        assert response.json().get('access_token'), "Token is not received!"
        return {"Authorization": f"Bearer {response.json().get('access_token')}"}
