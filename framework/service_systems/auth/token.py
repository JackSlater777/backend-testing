import requests
from http import HTTPStatus


class Token:
    def __init__(self, url):
        self.service_name = "token"
        self.url = url

    def get_bearer_token(self, payload: str) -> dict:
        """Get a bearer_token token"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = "/auth/realms/APIGW_API/protocol/openid-connect/token"
        response = requests.post(url=self.url+url, headers=headers, data=payload)
        assert response.status_code == HTTPStatus.OK, f"Unexpected status received: {response.status_code}"
        assert response.json().get('access_token'), "Token is not received!"
        return {"Authorization": f"Bearer {response.json().get('access_token')}"}
