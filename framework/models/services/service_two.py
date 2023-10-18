# module used: datamodel-code-generator
# To generate pydantic-schema.py from json, run:
# datamodel-codegen --input name.json --output schema.py

from typing import List
from pydantic import Field, root_validator, conint, confloat
from src.models.common import Base


class UnitOfMeasure(Base):
    units: str = Field(default='Рубль')
    amount: confloat(strict=True) = Field(default=1.0)


class TaxItem(Base):
    tax_amount: confloat(strict=True) = Field(default=0.0, alias='taxAmount')
    tax_category: str = Field(default='VAT', alias='taxCategory')
    price_tax_excluded: confloat(strict=True) = Field(default=0.0, alias='priceTaxExcluded')


class Price(Base):
    unit: str = Field(default='Ruble')
    value: confloat(strict=True) = Field(default=0.0)


class ValidFor(Base):
    start_date_time: str = Field(default='2021-04-05T00:00:00Z', alias='startDateTime')
    end_date_time: str = Field(default='9999-12-31T23:59:59.999Z', alias='endDateTime')


class V1HandlerTwoHttpResponse(Base):
    id: str
    href: str
    base_type: str = Field(default='ProductOfferingPrice', alias='@baseType')
    field_type: str = Field(default='ProductOfferingPrice', alias='@type')
    code: str = Field(default='Test_code')
    description: str = Field(default='Test Description')
    is_bundle: bool = Field(default=False, alias='isBundle')
    offset: conint(strict=True) = Field(default=0)
    prod_spec_char_value_use: List = Field(default=list(), alias='prodSpecCharValueUse')
    version: str = Field(default='1.0')
    lifecycle_status: str = Field(default='Active', alias='lifecycleStatus')
    created_on: str = Field(default='2021-04-05T00:00:00Z', alias='createdOn')
    created_by: str = Field(default='Eduard.Shamanin', alias='createdBy')
    percentage: confloat(strict=True) = Field(default=0.0)
    tarification_tag: str = Field(alias='tarificationTag')
    name: str = Field(default='Test Product Offering')
    product_status: str = Field(default='ACTIVE_TRIAL', alias='productStatus')
    price: Price = Field(default_factory=Price)
    duration: conint(strict=True) = Field(default=1)
    price_type: str = Field(default='RecurringCharge', alias='priceType')
    recurring_charge_period_type: str = Field(default='month', alias='recurringChargePeriodType')
    recurring_charge_period_length: conint(strict=True) = Field(default=6, alias='recurringChargePeriodLength')
    tax: List[TaxItem] = Field(default=[TaxItem()])
    unit_of_measure: UnitOfMeasure = Field(default_factory=UnitOfMeasure, alias='unitOfMeasure')
    valid_for: ValidFor = Field(default_factory=ValidFor, alias='validFor')

    @root_validator(pre=True)
    def build_href(cls, values):
        values['href'] = f'/api/price-catalog-management/v1/productOfferingsPrices/{values["id"]}'
        return values


class V1HandlerTwoHttpResponse400(Base):
    service_name: str = Field(default="service_one", alias="serviceName")
    error_code: str = Field(default="BAD_REQUEST", alias="errorCode")
    user_message: str = Field(default="Wrong attributes value or mandatory attributes missing", alias="userMessage")


class V1HandlerTwoHttpResponse500(Base):
    service_name: str = Field(default="service_one", alias="serviceName")
    error_code: str = Field(default="InternalServerError", alias="errorCode")
    user_message: str = Field(default="Internal error from catalog service", alias="userMessage")
