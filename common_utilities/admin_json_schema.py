from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError


######################################################################################################
admin_login_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string"
        },
        "password": {
            "type": "string",
            "minLength": 8
        }

    },
    "required": ["email", "password"],
    "additionalProperties": False
}

def admin_login(data):
    try:
        validate(instance=data, schema=admin_login_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "messgae": e.message}
    return {"result": True, "data": data}
######################################################################################################

######################################################################################################
admin_register_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string"
        },
        "password": {
            "type": "string",
            "minLength": 8
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
    },
    "required": ["email", "password", "first_name", "last_name"],
    "additionalProperties": False
}

def admin_register(data):
    try:
        validate(instance=data, schema=admin_register_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "messgae": e.message}
    return {"result": True, "data": data}
######################################################################################################