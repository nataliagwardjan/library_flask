import uuid

from jsonschema.validators import Draft7Validator

from app import app
from flask import request, jsonify

from main.const.global_const import VALUE_ERROR
from main.validator.json_schema_validator import json_schema_validator
from main.exception.exception import BasicException
from main.service.user_service import add_new_user, get_user_by_id_from_db, get_all_users, \
    update_user_roles_by_user_id, delete_user_by_id, update_user_by_user_id
from main.const.json_schemas import request_add_user_schema, response_schema, response_get_user_schema, \
    response_get_users_schema, request_update_user_roles_schema, request_update_user_schema


@app.route('/users', methods=['GET'])
def get_users():
    try:
        response = get_all_users()
        json_schema_validator(response, response_get_users_schema)
    except BasicException as e:
        response = {
            "response_type": e.exception_type,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
    return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400


@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id: uuid):
    try:
        response = get_user_by_id_from_db(user_id)
        json_schema_validator(response, response_get_user_schema)
    except BasicException as e:
        response = {
            "response_type": e.exception_type,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
    return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400


@app.route('/users', methods=['POST'])
def add_user():
    user = request.get_json()
    validator = Draft7Validator(request_add_user_schema)
    errors = sorted(validator.iter_errors(user), key=lambda error: error.path)
    if errors:
        error_messages = [{"message": error.message, "path": list(error.path)} for error in errors]
        response = {
            "response_type": VALUE_ERROR,
            "message": f"{error_messages}",
            "http_status_code": 400
        }
        return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400

    try:
        response = add_new_user(user)
        json_schema_validator(response, response_schema)
    except BasicException as e:
        response = {
            "response_type": e.exception_type,
            "message": f"Exception: {e.message}",
            "http_status_code": 400
        }
    return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400


@app.route('/users/<user_id>/update_roles', methods=['PATCH'])
def roles_update_user(user_id: uuid):
    update_user_roles = request.get_json()
    validator = Draft7Validator(request_update_user_roles_schema)
    errors = sorted(validator.iter_errors(update_user_roles), key=lambda error: error.path)
    if errors:
        error_messages = [{"message": error.message, "path": list(error.path)} for error in errors]
        response = {
            "response_type": VALUE_ERROR,
            "message": f"{error_messages}",
            "http_status_code": 400
        }
        return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400

    try:
        roles_list = update_user_roles["roles"]
        response = update_user_roles_by_user_id(user_id, roles_list)
        json_schema_validator(response, response_schema)
    except BasicException as e:
        response = {
            "response_type": e.exception_type,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
    return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400


@app.route('/users/<user_id>', methods=['DELETE'])
def remove_user_by_id(user_id: uuid):
    try:
        response = delete_user_by_id(user_id)
        json_schema_validator(response, response_schema)
        print(response)
    except BasicException as e:
        response = {
            "response_type": e.exception_type,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
        print(response)
    return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400


@app.route('/users/<user_id>', methods=['PUT'])
def update_user_by_id(user_id: uuid):
    request_update_user = request.get_json()
    validator = Draft7Validator(request_update_user_schema)
    errors = sorted(validator.iter_errors(request_update_user), key=lambda error: error.path)
    if errors:
        error_messages = [{"message": error.message, "path": list(error.path)} for error in errors]
        response = {
            "response_type": VALUE_ERROR,
            "message": f"{error_messages}",
            "http_status_code": 400
        }
        return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400

    try:
        user_update = {
            "name": request_update_user["name"],
            "surname": request_update_user["surname"],
            "email": request_update_user["email"]
        }
        response = update_user_by_user_id(user_id, user_update)
        json_schema_validator(response, response_schema)
    except BasicException as e:
        response = {
            "response_type": e.exception_type,
            "message": f"Exception: {e}",
            "http_status_code": 400
        }
    return jsonify(response), response['http_status_code'] if response['http_status_code'] else 400


# todo - /users/<user_id> PUT
"""request_update_user_schema"""
# JSON schema
"""
    {
        "name": "John",
        "surname": "Smith",
        "email": "john.smith@email.com"
    }
"""

# todo - /users/<id>/change_password PATCH
"""request_update_user_password_schema"""
# JSON schema
"""
    {
        "current_password": "my_Current_p@ssword",
        "new_password": "my_New_p@ssword!",
        "repeat_new_password": "my_New_p@ssword!"
    }
"""
