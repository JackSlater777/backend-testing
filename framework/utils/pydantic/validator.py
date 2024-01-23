import allure


class PydanticValidator:
    @staticmethod
    def validate_response_schema(response_schema, response):
        with allure.step("Response validating"):
            assert response_schema.model_validate(response), \
                "The response from the service does not match the schema!"
