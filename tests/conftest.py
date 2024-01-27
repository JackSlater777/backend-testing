import pytest
from config.setup_config import setup_config


def pytest_addoption(parser) -> None:
    """Declaring the command-line options for test run"""
    parser.addoption("--env", default="localhost")


@pytest.fixture(scope="session")
def setup_zone_params(request) -> dict:
    zone = request.config.getoption("--env")
    if not zone:
        pytest.exit("Не указан параметр --env")
    return setup_config(zone=zone)
