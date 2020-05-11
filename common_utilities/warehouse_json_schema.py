from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

######################################################################################################
users_warehouse_schema = {
    "type": "object",
    "properties": {
        "nodes": {
            "type": "object"
        },
        "size": {
            "type": "string"
        },
        "address": {
                    "type": "string"
                },
        "active": {
                    "type": "boolean"
                },
        "latitude": {
                    "type": "string"
                },
        "longitude": {
                    "type": "string"
                },
        "cargo_capacity": {
                    "type": "string"
                },
        "email": {
                    "type": "string"
                },
    },
    "required": ["nodes", "size", "address", "active", "latitude", "longitude",
                 "cargo_capacity", "email"],
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
