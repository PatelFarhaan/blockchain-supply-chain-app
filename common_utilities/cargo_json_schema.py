from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

######################################################################################################
users_cargo_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        }
    },
    "required": ["name"],
    "additionalProperties": False
}


def validate_user_cargo(data):
    try:
        validate(instance=data, schema=users_cargo_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "messgae": e.message}
    return {"result": True, "data": data}
######################################################################################################
