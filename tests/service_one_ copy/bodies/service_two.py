from src.models.catalog.current_price.response import CatalogCurrentPriceResponse
from src.enums.common import MockCurrentPriceItemId, TarificationTag


class ResponseBody:

    class V1HandlerOne:
        def day(self):
            return CatalogCurrentPriceResponse(
                id=MockCurrentPriceItemId.DAY,
                tarification_tag=TarificationTag.DAY
            ).dict(by_alias=True)
