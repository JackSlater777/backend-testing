from framework.service_systems.auth.token import Token
from config.setup_config import get_credentials_for_bearer_token


class Auth:
    def __init__(self):
        # self.token = None
        self.bearer_token = None

    def get_bearer_token(self) -> dict:
        if not self.bearer_token:
            self.bearer_token = Token.get_bearer_token(payload=get_credentials_for_bearer_token())
        return self.bearer_token


auth = Auth()
