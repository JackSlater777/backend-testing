import pytest
from framework.handlers.http.trading_app import TradingAppHttpClient


@pytest.fixture(scope="session")
def trading_app_http_client(setup_zone_params):
    return TradingAppHttpClient(
        url=setup_zone_params.get("trading_app").get("address")
    )
