# module used: datamodel-code-generator
# To generate pydantic-schema.py from json, run:
# datamodel-codegen --input name.json --output schema.py

from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        # Allows to transfer parameters into builder with "true" names, not aliases
        allow_population_by_field_name = True
