from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

######################################################################################################
users_sensor_schema = {
    "type": "object",
    "properties": {
        "sensor_id": {
            "type": "string"
        },
        "type": {
            "type": "string"
        },
        "weight": {
                    "type": "number"
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
        "barcode_id": {
                    "type": "string"
                },
        "temperature": {
                    "type": "number"
                },
    },
    "required": ["weight", "active", "latitude", "longitude", "barcode_id",
                 "temperature", "type", "sensor_id"],
    "additionalProperties": False
}


def validate_user_sensor(data):
    try:
        validate(instance=data, schema=users_sensor_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "message": e.message}
    return {"result": True, "data": data}

######################################################################################################
