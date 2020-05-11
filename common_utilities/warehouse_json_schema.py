from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

######################################################################################################
users_warehouse_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "location": {
            "type": "string"
        }
    },
    "required": ["name", "location"],
    "additionalProperties": False
}


def validate_user_warehouse(data):
    try:
        validate(instance=data, schema=users_warehouse_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "message": e.message}
    return {"result": True, "data": data}
######################################################################################################
