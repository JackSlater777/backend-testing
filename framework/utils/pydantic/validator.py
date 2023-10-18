import allure
from pydantic import BaseModel
from src.models.config import Base


class PydanticValidator:
    @staticmethod
    def validate_response_schema(response_schema: BaseModel | Base, response: dict | list):
        with allure.step("Response validating"):
            assert response_schema.parse_obj(response), \
                "The response from the service does not match the schema!"
