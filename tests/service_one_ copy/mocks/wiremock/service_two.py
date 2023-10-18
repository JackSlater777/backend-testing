from http import HTTPStatus
from src.models.wiremock.wiremock import Wiremock, Request, Response
from src.enums.common import MockCurrentPriceItemId, HTTPMethod, CurrentPriceScenarioName, NextPriceScenarioName
from tests.service_one.resource import Catalog
from tests.service_one.bodies.service_two import ResponseBody


service_two_v1_handler_one_resp_body = ResponseBody().V1HandlerOne()


class CatalogWiremock:
    class CurrentPrice:
        def day(self):
            return Wiremock(
                scenario_name=CurrentPriceScenarioName.DAY,
                request=Request(
                    method=HTTPMethod.GET,
                    url=Catalog.current_price_url + MockCurrentPriceItemId.DAY
                ),
                response=Response(
                    json_body=service_two_v1_handler_one_resp_body.day(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def month(self):
            return Wiremock(
                scenario_name=CurrentPriceScenarioName.MONTH,
                request=Request(
                    method=HTTPMethod.GET,
                    url=Catalog.current_price_url + MockCurrentPriceItemId.MONTH
                ),
                response=Response(
                    json_body=service_two_v1_handler_one_resp_body.month(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def year(self):
            return Wiremock(
                scenario_name=CurrentPriceScenarioName.YEAR,
                request=Request(
                    method=HTTPMethod.GET,
                    url=Catalog.current_price_url + MockCurrentPriceItemId.YEAR
                ),
                response=Response(
                    json_body=service_two_v1_handler_one_resp_body.year(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def error_400(self):
            return Wiremock(
                scenario_name=CurrentPriceScenarioName.CATALOG_400,
                request=Request(
                    method=HTTPMethod.GET,
                    url=Catalog.current_price_url + MockCurrentPriceItemId.CATALOG_400
                ),
                response=Response(
                    json_body=service_two_v1_handler_one_resp_body.error_400(),
                    status=HTTPStatus.BAD_REQUEST
                )
            ).dict(by_alias=True, exclude_none=True)


        def error_500(self):
            return Wiremock(
                scenario_name=CurrentPriceScenarioName.CATALOG_500,
                request=Request(
                    method=HTTPMethod.GET,
                    url=Catalog.current_price_url + MockCurrentPriceItemId.CATALOG_500
                ),
                response=Response(
                    json_body=service_two_v1_handler_one_resp_body.error_500(),
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )
            ).dict(by_alias=True, exclude_none=True)

    class NextPrice:
        def day(self):
            return Wiremock(
                scenario_name=NextPriceScenarioName.DAY,
                request=Request(
                    method=HTTPMethod.POST,
                    url=Catalog.next_price_url
                ),
                response=Response(
                    json_body=catalog_resp_body_np.day(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def month(self):
            return Wiremock(
                scenario_name=NextPriceScenarioName.MONTH,
                request=Request(
                    method=HTTPMethod.POST,
                    url=Catalog.next_price_url
                ),
                response=Response(
                    json_body=catalog_resp_body_np.month(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def year(self):
            return Wiremock(
                scenario_name=NextPriceScenarioName.YEAR,
                request=Request(
                    method=HTTPMethod.POST,
                    url=Catalog.next_price_url
                ),
                response=Response(
                    json_body=catalog_resp_body_np.year(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def error_400(self):
            return Wiremock(
                scenario_name=NextPriceScenarioName.CATALOG_400,
                request=Request(
                    method=HTTPMethod.POST,
                    url=Catalog.next_price_url
                ),
                response=Response(
                    json_body=catalog_resp_body_np.error_400(),
                    status=HTTPStatus.BAD_REQUEST
                )
            ).dict(by_alias=True, exclude_none=True)

        def error_424(self):
            return Wiremock(
                scenario_name=NextPriceScenarioName.CATALOG_424,
                request=Request(
                    method=HTTPMethod.POST,
                    url=Catalog.next_price_url
                ),
                response=Response(
                    json_body=catalog_resp_body_np.error_424(),
                    status=HTTPStatus.OK
                )
            ).dict(by_alias=True, exclude_none=True)

        def error_500(self):
            return Wiremock(
                scenario_name=NextPriceScenarioName.CATALOG_500,
                request=Request(
                    method=HTTPMethod.POST,
                    url=Catalog.next_price_url
                ),
                response=Response(
                    json_body=catalog_resp_body_np.error_500(),
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )
            ).dict(by_alias=True, exclude_none=True)
