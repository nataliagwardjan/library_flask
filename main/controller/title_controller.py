import uuid

from jsonschema.validators import Draft7Validator

from app import app
from flask import request, jsonify


@app.route('/titles', methods=['GET'])
def get_titles():
    return "<h1>TITLES!</h1>"
