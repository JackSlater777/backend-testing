import pytest
from tests.service_one.resource import wiremock_api, catalog_wiremock_cp, pr_calc_req_body_cp


# @pytest.fixture(scope='session')
# def token():
#     return bearer_token.get_bearer_token(payload=payload, headers=headers)


@pytest.fixture
def mock_service_two_v1_handler_one_day():
    try:
        wiremock_api.create_mapping(mock=catalog_wiremock_cp.day())
        yield
    finally:
        wiremock_api.delete_mapping_by_scenario_name(mock=catalog_wiremock_cp.day())


@pytest.fixture
def v1_handler_one_body():
    return pr_calc_req_body_cp.day()
