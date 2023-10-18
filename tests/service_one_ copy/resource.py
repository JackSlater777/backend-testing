# After successfull testing these classes should be transferred to capybara submodule

import allure
import requests
import json
from http import HTTPStatus
from env_vars import APIGW_BASE_URL
from framework.utils.pydantic.validator import PydanticValidator
from framework.library.service_systems.apigw.token import Token
from framework.library.service_systems.wiremock.api import WiremockApi
from tests.service_one.config import payload, headers
from tests.service_one.bodies.service_one import PriceCalcRequestBody
from tests.service_one.mocks.wiremock.service_two import CatalogWiremock


class Catalog:
    # Basic url
    CATALOG_URL = "/api/catalog/catalogapp/v1"
    base_url = APIGW_BASE_URL + CATALOG_URL
    # API Methods
    current_price = "/productOfferingsPrices/"
    next_price = "/productOfferings"
    params = "?fields=id,name,productOfferingPrice"
    # Compound urls for mock building
    current_price_url = CATALOG_URL + current_price
    next_price_url = CATALOG_URL + next_price + params


pydantic_validator = PydanticValidator()
bearer = Token()
wiremock_api = WiremockApi()
catalog_wiremock_cp = CatalogWiremock().CurrentPrice()
pr_calc_req_body_cp = PriceCalcRequestBody().CurrentPrice()
