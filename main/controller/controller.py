import uuid

from jsonschema.validators import Draft7Validator

from app import app
from flask import request, jsonify
from jsonschema import validate, ValidationError

from main.const.global_const import WRONG_DATA_FIELD_IN_REQUEST, EXCEPTION_HANDLE, JSON_SCHEMA_VALIDATION_FAILED
from main.exception.basic_exception import BasicException
from main.exception.json_schema_validate_exception import JSONSchemaValidateException
from main.service.user_service import add_new_user, get_user_by_id_from_db, get_all_users
from main.const.json_schemas import add_user_schema, response_schema, response_get_user_schema, \
    response_get_users_schema


@app.route('/users', methods=['GET'])
def get_users():
    try:
        response = get_all_users()
        json_schema_validator(response, response_get_users_schema)
    except BasicException as e:
        response = {
            "response_type": JSON_SCHEMA_VALIDATION_FAILED,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
        json_schema_validator(response, response_schema)
    return jsonify(response), response['http_status_code']


@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id: uuid):
    try:
        response = get_user_by_id_from_db(user_id)
        json_schema_validator(response, response_get_user_schema)
    except BasicException as e:
        response = {
            "response_type": JSON_SCHEMA_VALIDATION_FAILED,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
        json_schema_validator(response, response_schema)
    return jsonify(response), response['http_status_code']


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


@app.route('/users/<user_id>/update_roles', methods=['PATCH'])
def roles_update_user(user_id: uuid):
    update_user_roles = request.get_json()
    validator = Draft7Validator(add_user_schema)
    errors = sorted(validator.iter_errors(update_user_roles), key=lambda e: e.path)
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
