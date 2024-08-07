import pytest
from config.setup_config import setup_config
from framework.service_systems.auth.token import Token
from config.setup_config import get_credentials_for_bearer_token


def pytest_addoption(parser) -> None:
    """Declaring the command-line options for test run"""
    parser.addoption("--env", default="localhost")
    # сюда можно добавлять кастомные аргументы, например логин и пароль (альтернатива env-файлам)

# можно добавить доп.фикстуры с логикой для обработки кастомных аргументов


@pytest.fixture(scope="session")
def setup_zone_params(request) -> dict:
    zone = request.config.getoption("--env")
    if not zone:
        pytest.exit("--env parameter is not defined!")
    return setup_config(zone=zone)


@pytest.fixture(scope="session")
def bearer_token(setup_zone_params):
    """Get Bearer token, sends in headers"""
    auth_http_client = Token(url=setup_zone_params.get("fsso").get("address"))
    return auth_http_client.get_bearer_token(payload=get_credentials_for_bearer_token())
