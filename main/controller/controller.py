from jsonschema.validators import Draft7Validator

from app import app
from flask import request, jsonify
from jsonschema import validate, ValidationError

from main.const.json_schemas import add_user_schema


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
        return jsonify({"errors": error_messages}), 400

    return jsonify({"received": user}), 201


@app.route('/titles', methods=['GET'])
def get_titles():
    return "<h1>TITLES!</h1>"
