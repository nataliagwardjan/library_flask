from main.exception.exception import JSONSchemaValidateException
from jsonschema import validate, ValidationError


def json_schema_validator(given_schema: dict, correct_schema: dict):
    try:
        validate(instance=given_schema, schema=correct_schema)
    except ValidationError as e:
        print(f"Object has not been validate by json schema: {e}")
        raise JSONSchemaValidateException(f"{e}")
