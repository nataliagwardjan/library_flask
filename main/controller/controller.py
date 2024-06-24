from jsonschema.validators import Draft7Validator

from app import app
from flask import request, jsonify
from jsonschema import validate, ValidationError

from main.const.global_const import WRONG_DATA_FIELD_IN_REQUEST, EXCEPTION_HANDLE
from main.exception.basic_exception import BasicException
from main.exception.json_schema_validate_exception import JSONSchemaValidateException
from main.service.user_service import add_new_user
from main.const.json_schemas import add_user_schema, response_schema


@app.route('/users', methods=['GET'])
def get_users():
    return "<h1>USERS!</h1>"


@app.route('/users', methods=['POST'])
def add_user():
    user = request.get_json()
    validator = Draft7Validator(add_user_schema)
    errors = sorted(validator.iter_errors(user), key=lambda e: e.path)
    if errors:
        error_messages = [{"message": error.message, "path": list(error.path)} for error in errors]
        response = {
            "response_type": WRONG_DATA_FIELD_IN_REQUEST,
            "message": f"{error_messages}",
            "http_status_code": 400
        }
        return jsonify(response), response['http_status_code']

    try:
        response = add_new_user(user)
        json_schema_validator(response, response_schema)
    except BasicException as e:
        response = {
            "response_type": EXCEPTION_HANDLE,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
        json_schema_validator(response, response_schema)
    return jsonify(response), response['http_status_code']


@app.route('/titles', methods=['GET'])
def get_titles():
    return "<h1>TITLES!</h1>"


def json_schema_validator(given_schema: dict, correct_schema: dict):
    try:
        validate(instance=given_schema, schema=correct_schema)
        print(f"Object has been validate by json schema")
    except ValidationError as e:
        print(f"Object has not been validate by json schema: {e}")
        raise JSONSchemaValidateException(f"{e}")