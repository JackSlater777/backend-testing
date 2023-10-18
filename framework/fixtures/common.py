import os
import pytest

option_list = {
    "team.terminal.address",
    "team.extra_headers",
    "collect_traces",
    "service_custom_urls"
}


def pytest_addoption(parser):
    pass


@pytest.fixture
def team_extra_headers(request):
    return request.config.getoption("team.extra_headers")
