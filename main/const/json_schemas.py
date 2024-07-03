response_schema = {
    "type": "object",
    "properties": {
        "response_type": {"type": "string"},
        "code": {"type": "string"},
        "message": {"type": "string"},
        "http_status_code": {
            "type": "integer",
            "minimum": 100,
            "exclusiveMaximum": 600
        }
    },
    "required": ["response_type", "message", "http_status_code"],
    "additionalProperties": {"type": "string"}
}

request_add_user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 2
        },
        "surname": {
            "type": "string",
            "minLength": 2
        },
        "email": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "password": {"type": "string"}
    },
    "required": ["name", "surname", "email", "password"],
    "additionalProperties": False
}

get_user_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        },
        "name": {
            "type": "string",
            "minLength": 2
        },
        "surname": {
            "type": "string",
            "minLength": 2
        },
        "email": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "roles": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["id", "name", "surname", "email", "roles"],
    "additionalProperties": {"type": "string"}
}

response_get_user_schema = {
    "type": "object",
    "properties": {
        "response_type": {"type": "string"},
        "code": {"type": "string"},
        "message": {"type": "string"},
        "http_status_code": {
            "type": "integer",
            "minimum": 100,
            "exclusiveMaximum": 600
        },
        "user": get_user_schema
    },
    "required": ["response_type", "message", "http_status_code", "user"],
    "additionalProperties": {"type": "string"}
}

response_get_users_schema = {
    "type": "object",
    "properties": {
        "response_type": {"type": "string"},
        "code": {"type": "string"},
        "message": {"type": "string"},
        "http_status_code": {
            "type": "integer",
            "minimum": 100,
            "exclusiveMaximum": 600
        },
        "users": {
            "type": "array",
            "items": get_user_schema,
            "uniqueItems": True
        },
        "page": {
            "type": "integer",
            "minimum": 1
        },
        "users_per_page": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        },
        "all_pages": {
            "type": "integer",
            "minimum": 1
        },
        "number_of_all_users": {
            "type": "integer",
            "minimum": 1
        }
    },
    "required": ["response_type", "message", "http_status_code", "users"],
    "additionalProperties": {"type": "string"}
}

update_user_roles_schema = {
    "type": "object",
    "properties": {
        "roles": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["roles"],
    "additionalProperties": {"type": "string"}
}

add_author_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 2
        },
        "surname": {
            "type": "string",
            "minLength": 2
        }
    },
    "required": ["name", "surname"],
    "additionalProperties": False
}

get_author_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        },
        "name": {
            "type": "string",
            "minLength": 2
        },
        "surname": {
            "type": "string",
            "minLength": 2
        },
        "number_of_titles": {
            "type": "integer",
            "minimum": 1
        }
    },
    "required": ["id", "name", "surname"],
    "additionalProperties": {"type": "string"}
}

get_title_short_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        },
        "title": {
            "type": "string",
            "minLength": 2
        },
        "author": get_author_schema,
        "publisher": {
            "type": "string",
            "minLength": 2
        },
        "year": {
            "type": "integer",
            "minimum": 1600,
            "maximum": 2100
        },
        "description": {"type": "string"},
        "categories": {
            "type": "array",
            "items": {"type": "string"},
            "uniqueItems": True
        }
    },
    "required": ["id", "title", "author", "publisher", "year", "description", "categories"],
    "additionalProperties": {"type": "string"}
}

get_title_long_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        },
        "title": {
            "type": "string",
            "minLength": 2
        },
        "author": get_author_schema,
        "publisher": {
            "type": "string",
            "minLength": 2
        },
        "year": {
            "type": "integer",
            "minimum": 1600,
            "maximum": 2100
        },
        "description": {"type": "string"},  # here will be long description
        "categories": {
            "type": "array",
            "items": {"type": "string"},
            "uniqueItems": True
        },
        "number_of_copies": {
            "type": "integer",
            "minimum": 1
        },
        "number_of_available_copies": {
            "type": "integer",
            "minimum": 1
        },
        "audiobook": {"type": "boolean"},
        "ebook": {"type": "boolean"}
    },
    "required": ["id", "title", "author", "publisher", "year", "description", "categories"],
    "additionalProperties": {"type": "string"}
}


