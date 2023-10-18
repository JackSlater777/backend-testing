# module used: datamodel-code-generator
# To generate pydantic-schema.py from json, run:
# datamodel-codegen --input name.json --output schema.py

from typing import Union, Optional, Dict, List
from pydantic import Field, conint
from src.models.config import Base


class ContentType(Base):
    equal_to: str = Field(default='application/json', alias='equalTo')
    case_insensitive: Optional[bool] = Field(alias='caseInsensitive')


class RequestHeaders(Base):
    content_type: ContentType = Field(alias='Content-Type')


class SearchTermCase(Base):
    matches: Optional[str]
    does_not_match: Optional[str] = Field(alias='doesNotMatch')


class SearchTerm(Base):
    search_term: SearchTermCase


class BodyPatterns(Base):
    equal_to_json: Union[Dict, List] = Field(alias='equalToJson')
    ignore_array_order: bool = Field(default=True, alias='ignoreArrayOrder')
    ignore_extra_elements: bool = Field(default=True, alias='ignoreExtraElements')


class BasicAuthCredentials(Base):
    username: str
    password: str


class Request(Base):
    method: str = Field(default='ANY')
    url: Optional[str]  # "url": "/your/url?and=query"
    url_pattern: Optional[str] = Field(alias='urlPattern')  # "urlPattern": "/your/([a-z]*)\\?and=query"
    url_path: Optional[str] = Field(alias='urlPath')  # "urlPath": "/your/url"
    url_path_pattern: Optional[str] = Field(alias='urlPathPattern')  # "urlPathPattern": "/your/([a-z]*)"
    headers: Optional[RequestHeaders]
    query_parameters: Optional[SearchTerm] = Field(alias='queryParameters')
    cookies: Optional[Dict]
    body_patterns: Optional[List[BodyPatterns]] = Field(alias='bodyPatterns')
    basic_auth_credentials: Optional[BasicAuthCredentials] = Field(alias='basicAuthCredentials')


class ResponseHeaders(Base):
    content_type: str = Field(default='application/json', alias='Content-Type')
    set_cookie: Optional[List] = Field(alias='Set-Cookie')
    cache_control: Optional[str] = Field(alias='Cache-Control')


class Response(Base):
    body: Optional[str]  # Literal text to put in the body
    json_body: Optional[Union[Dict, List]] = Field(alias='jsonBody')  # Json: or dict/list, or None
    body_file_name: Optional[str] = Field(alias='bodyFileName')  # path/to/file/with/body
    base64_body: Optional[str] = Field(alias='base64Body')  # base64 string
    headers: ResponseHeaders = Field(default_factory=ResponseHeaders)
    status: conint(strict=True)


class Wiremock(Base):
    scenario_name: str = Field(alias='scenarioName')
    priority: Optional[conint(strict=True)]
    request: Request = Field(default_factory=Request)
    response: Response = Field(default_factory=Response)
