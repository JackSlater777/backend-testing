from src.models.price_calc.current_price.request import PriceCalcCurrentPriceRequest, CurrentPriceItem
from src.enums.common import ProductOfferingId, MockCurrentPriceItemId


class PriceCalcRequestBody:

    class CurrentPrice:
        """Method /currentPrice"""
        def day(self):
            return PriceCalcCurrentPriceRequest(
                product_offering_id=ProductOfferingId.DAY,
                current_price=[
                    CurrentPriceItem(id=MockCurrentPriceItemId.DAY)
                ]
            ).dict(by_alias=True)
