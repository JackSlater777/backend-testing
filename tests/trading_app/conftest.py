import pytest
from framework.handlers.http.trading_app import TradingAppHttpClient


@pytest.fixture(scope="session")
def trading_app_http_client(setup_zone_params, bearer_token):
    return TradingAppHttpClient(
        url=setup_zone_params.get("trading_app").get("address"),
        token=bearer_token
    )
