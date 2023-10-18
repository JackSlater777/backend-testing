from framework.utils.enums import StrValueEnum


class TarificationTag(str, StrValueEnum):
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"


class ProductOfferingId(str, StrValueEnum):
    """For functional and integration tests"""
    DAY = "ffd19bf2-0c1d-48e1-a100-3f5f029e5130"
    MONTH = "d060cc50-9832-4f02-87ae-98137a53c0a3"
    YEAR = "2fb5ea06-1a1f-494a-94c4-724ba910d8bb"


class MockCurrentPriceItemId(str, StrValueEnum):
    """For functional tests - it leads into catalog mock"""
    DAY = "00189d04-acc1-438c-9d5a-cdc2e72b61d5"
    MONTH = "00289d04-acc1-438c-9d5a-cdc2e72b61d5"
    YEAR = "00389d04-acc1-438c-9d5a-cdc2e72b61d5"
    CATALOG_400 = "00489d04-acc1-438c-9d5a-cdc2e72b61d5"
    CATALOG_500 = "00589d04-acc1-438c-9d5a-cdc2e72b61d5"


class MockNextPriceItemId(str, StrValueEnum):
    """For functional tests - it leads into the object within "transitionsBetweenEntities" array"""
    DAY = "00789d04-acc1-438c-9d5a-cdc2e72b61d5"
    MONTH = "00889d04-acc1-438c-9d5a-cdc2e72b61d5"
    YEAR = "00989d04-acc1-438c-9d5a-cdc2e72b61d5"
    CATALOG_424 = "01089d04-acc1-438c-9d5a-cdc2e72b61d5"
    CATALOG_400 = "01189d04-acc1-438c-9d5a-cdc2e72b61d5"
    CATALOG_500 = "01289d04-acc1-438c-9d5a-cdc2e72b61d5"


class CurrentPriceItemId(str, StrValueEnum):
    """For integration tests"""
    DAY = "fd7d4ee6-4ceb-4e90-9e76-34f956574eb0"
    MONTH = "2f59f238-ae19-486a-81a2-34688b683d25"
    YEAR = "83c94ae5-8cf1-4949-96ce-884dc01491ca"
    CATALOG_424 = "c73be419-9ab1-4fe1-8150-34f7ae18f9e3"


class CurrentPriceScenarioName(str, StrValueEnum):
    """It's used for possibility to delete a mock"""
    DAY = "mock_catalog_current_price_day_200"
    MONTH = "mock_catalog_current_price_month_200"
    YEAR = "mock_catalog_current_price_year_200"
    CATALOG_400 = "mock_catalog_current_price_400"
    CATALOG_500 = "mock_catalog_current_price_500"


class NextPriceScenarioName(str, StrValueEnum):
    """It's used for possibility to delete a mock"""
    DAY = "mock_catalog_next_price_day_200"
    MONTH = "mock_catalog_next_price_month_200"
    YEAR = "mock_catalog_next_price_year_200"
    CATALOG_400 = "mock_catalog_next_price_400"
    CATALOG_424 = "mock_catalog_next_price_424"
    CATALOG_500 = "mock_catalog_next_price_500"


class HTTPMethod(str, StrValueEnum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
