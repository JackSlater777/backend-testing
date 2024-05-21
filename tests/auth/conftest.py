import pytest
from framework.service_systems.auth.token import Token


@pytest.fixture(scope="session")
def auth_http_client(setup_zone_params):
    return Token(
        url=setup_zone_params.get("fsso").get("address")
    )
