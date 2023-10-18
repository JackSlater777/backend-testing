# # module used: datamodel-code-generator
# # To generate pydantic-schema.py from json, run:
# # datamodel-codegen --input name.json --output schema.py
#
# from typing import List, Dict, Union, Optional
# from pydantic import BaseModel, Field, conint, confloat, validator
# from uuid import uuid4, UUID
# from datetime import datetime
# from src.enums.common import TarificationTag
# from src.models.config import Base
#
#
# class ClientInfo(Base):
#     party_id: Optional[str] = Field(default=None, alias='partyId')
#     party_role_id: str = Field(default='c938f7aa-19d3-43fc-8432-3212afb8d9e2', alias='partyRoleId')
#
#
# class UnitOfMeasure(Base):
#     units: str = Field(default='Рубль')
#     amount: confloat(strict=True) = Field(default=1.0)
#
#
# class TaxItem(Base):
#     tax_amount: confloat(strict=True) = Field(default=0.0, alias='taxAmount')
#     tax_category: str = Field(default='VAT', alias='taxCategory')
#     price_tax_excluded: confloat(strict=True) = Field(default=0.0, alias='priceTaxExcluded')
#
#
# class Price(Base):
#     unit: str = Field(default='Ruble')
#     value: confloat(strict=True) = Field(default=0.0)
#
#
# def validate_datetime_field(value):
#     DAY_TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
#     DAY_TIME_FORMAT_FRACTIONS: str = "%Y-%m-%dT%H:%M:%S.%fZ"
#
#     for t_format in (DAY_TIME_FORMAT, DAY_TIME_FORMAT_FRACTIONS):
#         try:
#             datetime.strptime(value, t_format)
#             return value
#         except ValueError:
#             pass
#     raise ValueError(f'Invalid datetime format: {value}. '
#                      f'Expected {DAY_TIME_FORMAT} or {DAY_TIME_FORMAT_FRACTIONS}')
#
#
# class ValidFor(Base):
#     start_date_time: str = Field(default='2021-04-05T00:00:00Z', alias='startDateTime')
#     end_date_time: str = Field(default='9999-12-31T23:59:59.999Z', alias='endDateTime')
#
#     _startDateTime = validator("startDateTime", allow_reuse=True)(validate_datetime_field)
#     _endDateTime = validator("endDateTime", allow_reuse=True)(validate_datetime_field)
#
#
# class NextEntity(Base):
#     id: str = Field(default='49489d04-acc1-438c-9d5a-cdc2e72b61d5')
#
#
# class CurrentPriceItem(Base):
#     id: Union[str, None]
#     price_alterations: List = Field(default=list(), alias='priceAlterations')
#     next_entity: NextEntity = Field(default_factory=NextEntity, alias='nextEntity')
#     name: str = Field(default='Test Product Offering')
#     product_status: str = Field(default='ACTIVE_TRIAL', alias='productStatus')
#     price: Price = Field(default_factory=Price)
#     duration: conint(strict=True) = Field(default=1)
#     price_type: str = Field(default='RecurringCharge', alias='priceType')
#     recurring_charge_period_type: str = Field(default='month', alias='recurringChargePeriodType')
#     recurring_charge_period_length: conint(strict=True) = Field(default=6, alias='recurringChargePeriodLength')
#     tax: List[TaxItem] = Field(default=[TaxItem()])
#     unit_of_measure: UnitOfMeasure = Field(default_factory=UnitOfMeasure, alias='unitOfMeasure')
#     valid_for: ValidFor = Field(default_factory=ValidFor, alias='validFor')
#
#
# class Context(Base):
#     id: str = Field(default='test_context_id')
#     phone_number: str = Field(default='9990123456', alias='phoneNumber')
#     status: str = Field(default='active')
#
#
# class V1HandlerOneHttpRequest(Base):
#     product_offering_id: str = Field(alias='productOfferingId')
#     client_info: ClientInfo = Field(default_factory=ClientInfo, alias='clientInfo')
#     order_date: str = Field(default='2023-03-03T10:59:57.687Z', alias='orderDate')
#     current_price: List[CurrentPriceItem] = Field(default=[CurrentPriceItem()], alias='currentPrice')
#     context: Dict = Field(default=dict())
#
#
# class CurrentPriceAlterations(BaseModel):
#     id: str
#     name: str
#     duration: Union[conint(strict=True), None]
#     percentage: conint(strict=True)
#     priceType: str
#     price: Price
#     recurringChargePeriodLength: conint(strict=True)
#     recurringChargePeriodType: str
#     validFor: ValidFor
#
#
# class Tax(BaseModel):
#     taxAmount: confloat(strict=True)
#     priceTaxExcluded: confloat(strict=True)
#     taxCategory: str
#
#
# class CurrentPriceOffer(BaseModel):
#     id: UUID = Field(default_factory=uuid4)
#     name: str
#     productStatus: str
#     price: Price
#     duration: Union[conint(strict=True), None]
#     priceType: str
#     recurringChargePeriodLength: conint(strict=True)
#     recurringChargePeriodType: str
#     tax: list[Tax]
#     unitOfMeasure: UnitOfMeasure
#     validFor: ValidFor
#     nextPayDate: str
#     tarificationTag: TarificationTag
#     priceAlterations: list[CurrentPriceAlterations]
#     nextEntity: NextEntity
#
#     _nextPayDate = validator("nextPayDate", allow_reuse=True)(validate_datetime_field)
#
#
# class V1HandlerOneHttpResponse(BaseModel):
#     currentPrice: list[CurrentPriceOffer]
