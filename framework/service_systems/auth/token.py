import requests
from http import HTTPStatus
from config import configuration


FSSO_BASE_URL = configuration.get("team.fsso.address")


class Token:
    @staticmethod
    def get_bearer_token(payload: str):
        """Get a bearer_token token"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = "/auth/realms/APIGW_API/protocol/openid-connect/token"
        response = requests.post(url=FSSO_BASE_URL+url, headers=headers, data=payload)
        assert response.status_code == HTTPStatus.OK, f"Unexpected status received: {response.status_code}"
        assert response.json().get('access_token') is not None, "Token is not received!"
        return {"Authorization": f"Bearer {response.json().get('access_token')}"}
